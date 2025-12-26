# Football Object Detection

This project utilizes object detection and tracking algorithms to analyze football match videos by detecting and tracking players, goalkeepers, referees, and other objects on the football pitch. The system uses **track-level jersey color clustering** to assign stable team identities to players.

## Demo
https://github.com/Mostafa-Nafie/Football-Object-Detection/assets/44211916/aaac347e-f21b-4433-841c-0cefea8770d2

## Quick Guide

<details><summary>Install</summary>
  
```
git clone https://github.com/Mostafa-Nafie/Football-Object-Detection.git
cd "./Football-Object-Detection"
pip install -r requirements.txt
```

</details>

<details><summary>Inference on video</summary>

To run the model on a video, run the following command: 
```
python main.py /path/to/video
```
The annotated video will be saved to the `./output/` folder with the format `{video_name}_out.mp4`

</details>

## Object Detection Model

The model used for object detection is [YOLOv8](https://github.com/ultralytics/ultralytics), trained on the [SoccerNet Dataset](https://drive.google.com/drive/folders/17w9yhEDZS7gLdZGjiwPQytLz3-iTUpKm) for 25 epochs. The model classifies objects into 6 different classes:

- **0** - Player  
- **1** - Goalkeeper  
- **2** - Ball  
- **3** - Main referee  
- **4** - Side referee  
- **5** - Staff members  

## How It Works

The system uses a **track-level team assignment approach** that provides stable and robust team identification. Here's how it works:

### Overview

Instead of assigning teams per detection or frame, the system:
1. Tracks players across frames using YOLOv8's built-in tracking
2. Accumulates jersey color samples for each track over multiple frames
3. Clusters tracks (not individual detections) to assign team identities
4. Maintains stable team assignments throughout the video

### Step-by-Step Process

#### **1. Object Detection and Tracking**

For each frame:
- YOLOv8 performs object detection to identify players, goalkeepers, ball, referees, and staff
- YOLOv8's tracking assigns stable **track IDs** to each player across frames
- Each player maintains the same track_id throughout their appearance in the video

#### **2. Grass Color Extraction** (First Frame Only)

From the first frame:
- The system extracts the dominant grass color by:
  - Converting the frame to HSV color space
  - Masking green colors (typical grass range)
  - Computing the average color of masked pixels
- This grass color is used to isolate jersey colors from the background

#### **3. Jersey Color Extraction** (Per Frame)

For each player detection with a valid track_id:
- The player's bounding box is cropped from the frame
- Grass color is removed using HSV color filtering
- The upper half of the player (jersey area) is focused on
- The average jersey color (BGR) is extracted
- **Color samples are accumulated per track_id** (not used immediately for team assignment)

#### **4. Track-Level Color Accumulation**

- Each track_id maintains a list of color samples collected over multiple frames
- Only bounding boxes with sufficient area (>500 pixels) are used to ensure quality
- Color samples are accumulated continuously as the video progresses

#### **5. Track-Level Clustering** (After Sufficient Data)

Once enough data is collected (typically after 30+ frames with at least 2 tracks):
- **One representative color per track** is computed using the median of accumulated samples
- **K-Means clustering (k=2)** is performed on track-level color vectors (not per-detection)
- Each track is assigned to **TeamA** or **TeamB** based on clustering
- The K-Means model is saved for assigning teams to new tracks

#### **6. Team Assignment and Visualization**

- **Stable Assignment**: Once a track is assigned to a team, it remains fixed
- **New Tracks**: Tracks appearing after clustering are assigned based on their color's distance to cluster centroids
- **Visualization**: Players are labeled as `"Player <track_id> | TeamA"` or `"Player <track_id> | TeamB"`
- **Unknown Tracks**: Tracks with insufficient color evidence are labeled as `"Unknown"`

### Key Advantages

✅ **Stable Team Identity**: Team assignment is a property of track_id, not individual detections  
✅ **Robust to Bad Frames**: One bad frame cannot flip a player's team  
✅ **Camera Orientation Independent**: No dependency on x-position or left/right heuristics  
✅ **Accurate**: Uses accumulated color samples over multiple frames for better accuracy  
✅ **Real-time Compatible**: Efficient implementation suitable for video processing  

### Technical Details

- **Tracking**: Uses YOLOv8's built-in tracker with `persist=True` for stable track IDs
- **Color Space**: BGR color space for jersey color representation
- **Clustering**: K-Means with k=2, using median aggregation for robustness
- **Minimum Samples**: Requires at least 3 color samples per track before clustering
- **Frame Threshold**: Waits for 30 frames before performing initial clustering

## Output Format

The annotated video displays:
- **Players**: `Player <track_id> | TeamA` or `Player <track_id> | TeamB`
- **Goalkeepers**: `GK <track_id>`
- **Other Objects**: `Ball`, `Main Ref`, `Side Ref`, `Staff`

Each object is drawn with a colored bounding box and label.

## Requirements

- Python 3.7+
- OpenCV
- NumPy
- Ultralytics YOLOv8
- scikit-learn

See `requirements.txt` for specific versions.

## Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed installation instructions
- **[Usage Guide](docs/USAGE.md)** - How to use the application and configure settings
- **[Contributing](CONTRIBUTING.md)** - Guidelines for contributing to the project
- **[Project Structure](PROJECT_STRUCTURE.md)** - Overview of the repository structure
- **[Changelog](CHANGELOG.md)** - Version history and changes

## Further Information

Detailed explanation of the model, training process, and implementation can be found in the Jupyter notebook (`Football_Object_Detection.ipynb`).
