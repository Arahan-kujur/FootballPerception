# Usage Guide

## Basic Usage

Process a video file:

```bash
python main.py path/to/your/video.mp4
```

The annotated video will be saved to `./output/{video_name}_out.mp4`

## Examples

### Process a test video

```bash
python main.py test_videos/CityUtdR.mp4
```

### Process a video with custom output path

Modify `main.py` to change the output directory, or update the `annotate_video` function.

## Command Line Arguments

Currently, the script accepts one argument:
- **Video path**: Path to the input video file

Example:
```bash
python main.py /path/to/video.mp4
```

## Output

The processed video will contain:
- **Players**: Labeled as `Player <track_id> | TeamA` or `Player <track_id> | TeamB`
- **Goalkeepers**: Labeled as `GK <track_id>`
- **Other objects**: Ball, Main Ref, Side Ref, Staff

Each object is drawn with a colored bounding box.

## Configuration

### Adjusting Detection Confidence

Edit `main.py` and change the confidence threshold:

```python
result = model.track(annotated_frame, conf=0.5, verbose=False, persist=True)[0]
# Change 0.5 to your desired confidence (0.0 to 1.0)
```

### Adjusting Clustering Parameters

Edit `main.py` to modify clustering behavior:

```python
min_samples_per_track = 3  # Minimum color samples before clustering
frames_before_clustering = 30  # Wait for some frames to accumulate data
```

### Changing Output Video Settings

Modify the video writer settings in `annotate_video`:

```python
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec
output_video = cv2.VideoWriter('./output/'+video_name.split('.')[0] + "_out.mp4",
                               fourcc,
                               30.0,  # FPS
                               (width, height))
```

## Performance Tips

1. **Use GPU**: If available, YOLOv8 will automatically use GPU for faster processing
2. **Reduce video resolution**: Lower resolution videos process faster
3. **Adjust confidence threshold**: Higher thresholds reduce false positives but may miss some detections
4. **Batch processing**: Process multiple videos by creating a simple script

## Troubleshooting

**Video won't open:**
- Ensure the video path is correct
- Check that the video format is supported (MP4, AVI, MOV)
- Install codec support if needed

**No detections:**
- Lower the confidence threshold
- Check that the model weights are correct
- Verify the video contains football match footage

**Poor team assignment:**
- Ensure sufficient frames are processed (30+)
- Check that players are clearly visible
- Verify jersey colors are distinct between teams

