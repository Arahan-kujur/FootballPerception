import cv2
import numpy as np
import sys
import os
from pathlib import Path
from ultralytics import YOLO
from sklearn.cluster import KMeans

def get_grass_color(img):
    """
    Finds the color of the grass in the background of the image

    Args:
        img: np.array object of shape (WxHx3) that represents the BGR value of the
        frame pixels .

    Returns:
        grass_color
            Tuple of the BGR value of the grass color in the image
    """
    # Convert image to HSV color space
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV
    lower_green = np.array([30, 40, 40])
    upper_green = np.array([80, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Calculate the mean value of the pixels that are not masked
    masked_img = cv2.bitwise_and(img, img, mask=mask)
    grass_color = cv2.mean(img, mask=mask)
    return grass_color[:3]

def extract_jersey_color(player_img, grass_hsv):
    """
    Extracts the jersey color from a single player bounding box image.
    
    Args:
        player_img: np.array object containing the BGR values of the cropped
        player bounding box.
        grass_hsv: np.array containing the HSV color value of the grass color.
    
    Returns:
        kit_color: np.array containing the BGR values of the jersey color
    """
    if player_img.size == 0:
        return None
    
    # Convert image to HSV color space
    hsv = cv2.cvtColor(player_img, cv2.COLOR_BGR2HSV)

    # Define range of green color in HSV (around grass color)
    lower_green = np.array([grass_hsv[0, 0, 0] - 10, 40, 40])
    upper_green = np.array([grass_hsv[0, 0, 0] + 10, 255, 255])

    # Threshold the HSV image to get only green colors
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # Bitwise-AND mask and original image (invert to remove grass)
    mask = cv2.bitwise_not(mask)
    # Focus on upper half of player (jersey area)
    upper_mask = np.zeros(player_img.shape[:2], np.uint8)
    upper_mask[0:player_img.shape[0]//2, 0:player_img.shape[1]] = 255
    mask = cv2.bitwise_and(mask, upper_mask)

    kit_color = np.array(cv2.mean(player_img, mask=mask)[:3])
    return kit_color

def compute_track_colors(track_color_samples):
    """
    Computes representative color for each track from accumulated samples.
    
    Args:
        track_color_samples: dict mapping track_id -> list of color vectors
    
    Returns:
        track_colors: dict mapping track_id -> representative color vector
    """
    track_colors = {}
    for track_id, color_samples in track_color_samples.items():
        if len(color_samples) > 0:
            # Use median for robustness against outliers
            track_colors[track_id] = np.median(color_samples, axis=0)
    return track_colors

def cluster_tracks_and_assign_teams(track_colors, min_samples=5):
    """
    Clusters tracks by jersey color and assigns team IDs.
    
    Args:
        track_colors: dict mapping track_id -> color vector
        min_samples: minimum number of color samples required for team assignment
    
    Returns:
        track_team_map: dict mapping track_id -> team_id ("TeamA", "TeamB", or "Unknown")
        kmeans_model: fitted KMeans model (or None if clustering failed)
    """
    track_team_map = {}
    
    # Filter tracks with sufficient color evidence
    valid_tracks = {tid: color for tid, color in track_colors.items() 
                    if color is not None and not np.isnan(color).any()}
    
    if len(valid_tracks) < 2:
        # Not enough tracks to cluster, assign all as Unknown
        for track_id in track_colors.keys():
            track_team_map[track_id] = "Unknown"
        return track_team_map, None
    
    # Prepare data for clustering
    track_ids = list(valid_tracks.keys())
    color_vectors = np.array([valid_tracks[tid] for tid in track_ids])
    
    # Run K-Means clustering with k=2
    kmeans = KMeans(n_clusters=2, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(color_vectors)
    
    # Map cluster 0 -> TeamA, cluster 1 -> TeamB
    for i, track_id in enumerate(track_ids):
        if cluster_labels[i] == 0:
            track_team_map[track_id] = "TeamA"
        else:
            track_team_map[track_id] = "TeamB"
    
    # Assign Unknown to tracks without valid colors
    for track_id in track_colors.keys():
        if track_id not in track_team_map:
            track_team_map[track_id] = "Unknown"
    
    return track_team_map, kmeans

def assign_team_to_new_track(track_color, kmeans_model):
    """
    Assigns team to a new track based on distance to cluster centroids.
    
    Args:
        track_color: color vector for the track
        kmeans_model: fitted KMeans model
    
    Returns:
        team_id: "TeamA", "TeamB", or "Unknown"
    """
    if kmeans_model is None or track_color is None or np.isnan(track_color).any():
        return "Unknown"
    
    # Predict cluster for this color
    cluster_label = kmeans_model.predict([track_color])[0]
    
    if cluster_label == 0:
        return "TeamA"
    else:
        return "TeamB"

def annotate_video(video_path, model, labels, box_colors):
    """
    Loads the input video and runs the object detection and tracking algorithm on its frames,
    accumulates jersey colors per track, clusters tracks for team assignment, and annotates frames.

    Args:
        video_path: String the holds the path of the input video
        model: Object that represents the trained object detection model
        labels: List of class labels
        box_colors: Dict mapping class index to color tuple
    Returns:
    """
    # Check if video file exists
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    cap = cv2.VideoCapture(video_path)
    
    # Check if video opened successfully
    if not cap.isOpened():
        raise ValueError(f"Could not open video file: {video_path}")

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    
    # Validate video dimensions
    if height <= 0 or width <= 0:
        cap.release()
        raise ValueError(f"Invalid video dimensions: {width}x{height}")

    # Cross-platform path handling
    video_path_obj = Path(video_path)
    video_name = video_path_obj.stem  # Get filename without extension
    
    # Ensure output directory exists
    output_dir = Path('./output')
    output_dir.mkdir(exist_ok=True)
    
    output_path = output_dir / f"{video_name}_out.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_video = cv2.VideoWriter(str(output_path),
                                   fourcc,
                                   30.0,
                                   (width, height))
    
    # Check if output video writer initialized successfully
    if not output_video.isOpened():
        cap.release()
        raise RuntimeError(f"Could not initialize video writer for: {output_path}")

    # Track-level color accumulation: track_id -> list of color vectors
    track_color_samples = {}
    
    # Track-level team assignment: track_id -> team_id
    track_team_map = {}
    
    # KMeans model for assigning teams to new tracks after clustering
    kmeans_model = None
    
    # Grass color for jersey extraction (computed once from first frame)
    grass_hsv = None
    grass_color_computed = False
    
    # Clustering parameters
    min_samples_per_track = 3  # Minimum color samples before clustering
    clustering_done = False
    frames_before_clustering = 30  # Wait for some frames to accumulate data

    frame_count = 0

    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            frame_count += 1
            # Run YOLOv8 tracking on the frame
            annotated_frame = cv2.resize(frame, (width, height))
            result = model.track(annotated_frame, conf=0.5, verbose=False, persist=True)[0]

            # Compute grass color from first frame
            if not grass_color_computed:
                grass_color = get_grass_color(result.orig_img)
                grass_hsv = cv2.cvtColor(np.uint8([[list(grass_color)]]), cv2.COLOR_BGR2HSV)
                grass_color_computed = True

            # Process each detection/track
            if result.boxes is not None and len(result.boxes) > 0:
                for box in result.boxes:
                    label = int(box.cls.numpy()[0])
                    x1, y1, x2, y2 = map(int, box.xyxy[0].numpy())
                    
                    # Get track_id if available (tracking is enabled)
                    track_id = None
                    if box.id is not None:
                        track_id = int(box.id.numpy()[0])
                    
                    # Only process players (label == 0) for team assignment
                    if label == 0 and track_id is not None and grass_hsv is not None:
                        # Extract jersey color from bounding box
                        player_img = result.orig_img[y1:y2, x1:x2]
                        
                        # Check if bounding box is large enough
                        bbox_area = (x2 - x1) * (y2 - y1)
                        min_bbox_area = 500  # Minimum area threshold
                        
                        if bbox_area >= min_bbox_area:
                            kit_color = extract_jersey_color(player_img, grass_hsv)
                            
                            if kit_color is not None and not np.isnan(kit_color).any():
                                # Initialize track color samples if needed
                                if track_id not in track_color_samples:
                                    track_color_samples[track_id] = []
                                
                                # Append color sample to track
                                track_color_samples[track_id].append(kit_color)
                    
                    # Perform clustering when enough data is collected
                    if (not clustering_done and 
                        frame_count >= frames_before_clustering and
                        len(track_color_samples) >= 2):
                        # Compute representative colors per track
                        track_colors = compute_track_colors(track_color_samples)
                        
                        # Cluster tracks and assign teams
                        track_team_map, kmeans_model = cluster_tracks_and_assign_teams(track_colors, min_samples_per_track)
                        clustering_done = True
                    
                    # For tracks that appear after clustering, assign team based on color
                    if clustering_done and label == 0 and track_id is not None:
                        if track_id not in track_team_map:
                            # Compute representative color for this track if we have samples
                            if track_id in track_color_samples and len(track_color_samples[track_id]) >= min_samples_per_track:
                                track_colors = compute_track_colors({track_id: track_color_samples[track_id]})
                                if track_id in track_colors:
                                    track_team_map[track_id] = assign_team_to_new_track(track_colors[track_id], kmeans_model)
                            else:
                                # Not enough samples yet, assign as Unknown
                                track_team_map[track_id] = "Unknown"
                    
                    # Visualization
                    # Determine display label and color based on detection class
                    if label == 0:  # Player
                        display_label = "Player"
                        color = box_colors["0"]
                        # Add track_id and team info if available
                        if track_id is not None:
                            team_id = track_team_map.get(track_id, "Unknown")
                            display_text = f"Player {track_id} | {team_id}"
                        else:
                            display_text = "Player"
                    elif label == 1:  # Goalkeeper
                        display_label = "GK"
                        color = box_colors["1"]
                        if track_id is not None:
                            display_text = f"GK {track_id}"
                        else:
                            display_text = "GK"
                    elif label == 2:  # Ball
                        display_label = labels[2]
                        color = box_colors["2"]
                        display_text = labels[2]
                    elif label == 3:  # Main Ref
                        display_label = labels[3]
                        color = box_colors["3"]
                        display_text = labels[3]
                    elif label == 4:  # Side Ref
                        display_label = labels[4]
                        color = box_colors["4"]
                        display_text = labels[4]
                    else:  # Staff (label == 5)
                        display_label = labels[5]
                        color = box_colors["5"]
                        display_text = labels[5]
                    
                    # Draw bounding box and label
                    cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), color, 2)
                    cv2.putText(annotated_frame, display_text, (x1 - 30, y1 - 10), 
                               cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

            # Write the annotated frame
            output_video.write(annotated_frame)

        else:
            # Break the loop if the end of the video is reached
            break

    cv2.destroyAllWindows()
    output_video.release()
    cap.release()

def main():
    """Main entry point for the application."""
    if len(sys.argv) < 2:
        print("Usage: python main.py <video_path>")
        print("Example: python main.py test_videos/CityUtdR.mp4")
        sys.exit(1)
    
    # Detection class labels (YOLO outputs: 0=Player, 1=GK, 2=Ball, 3=Main Ref, 4=Side Ref, 5=Staff)
    labels = ["Player", "GK", "Ball", "Main Ref", "Side Ref", "Staff"]
    box_colors = {
        "0": (150, 50, 50),      # Player
        "1": (41, 248, 165),     # GK
        "2": (155, 62, 157),     # Ball
        "3": (123, 174, 213),    # Main Ref
        "4": (217, 89, 204),     # Side Ref
        "5": (22, 11, 15)        # Staff
    }
    
    video_path = sys.argv[1]
    weights_path = Path("./weights/last.pt")
    
    # Check if weights file exists
    if not weights_path.exists():
        print(f"Error: Model weights not found at {weights_path}")
        print("Please ensure the model weights are in the weights/ directory")
        print("The file should be named 'last.pt'")
        sys.exit(1)
    
    try:
        print(f"Loading model from {weights_path}...")
        model = YOLO(str(weights_path))
        
        print(f"Processing video: {video_path}")
        annotate_video(video_path, model, labels, box_colors)
        
        output_path = Path("./output") / f"{Path(video_path).stem}_out.mp4"
        print(f"Processing complete! Output saved to: {output_path.absolute()}")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()