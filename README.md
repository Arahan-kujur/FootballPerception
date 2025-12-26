# ⚽ Football Object Detection

[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: PEP 8](https://img.shields.io/badge/code%20style-PEP%208-brightgreen.svg)](https://www.python.org/dev/peps/pep-0008/)

A robust football match video analysis system that uses **YOLOv8 object detection** and **track-level jersey color clustering** to detect, track, and assign team identities to players in football match videos.

## 🎯 Features

- **Object Detection**: Detects players, goalkeepers, ball, referees, and staff using YOLOv8
- **Player Tracking**: Stable track IDs assigned to each player across frames
- **Team Assignment**: Track-level jersey color clustering for accurate team identification
- **Stable Team Identity**: Team assignment remains consistent throughout the video
- **Robust Processing**: Handles occlusions, camera movements, and varying lighting conditions
- **Real-time Compatible**: Efficient implementation suitable for video processing

## 📋 Table of Contents

- [Installation](#-installation)
- [Quick Start](#-quick-start)
- [Usage](#-usage)
- [How It Works](#-how-it-works)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Documentation](#-documentation)
- [Contributing](#-contributing)
- [License](#-license)

## 🚀 Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/Football-Object-Detection.git
cd Football-Object-Detection
```

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Download Model Weights

Download the trained YOLOv8 model weights and place them in the `weights/` directory:

```bash
# Ensure weights/last.pt exists
# The model should be trained on SoccerNet dataset with 6 classes
```

For detailed installation instructions, see [Installation Guide](docs/INSTALLATION.md).

## ⚡ Quick Start

1. **Prepare your video**: Place your football match video in the project directory or provide the full path

2. **Run the detection**:
   ```bash
   python main.py path/to/your/video.mp4
   ```

3. **Find the output**: The annotated video will be saved in `./output/{video_name}_out.mp4`

### Example

```bash
python main.py test_videos/CityUtdR.mp4
```

## 📖 Usage

### Basic Usage

```bash
python main.py <video_path>
```

### Command Line Options

The script accepts one required argument:
- **`<video_path>`**: Path to the input video file (MP4, AVI, MOV formats supported)

### Output

The processed video contains:
- **Players**: Labeled as `Player <track_id> | TeamA` or `Player <track_id> | TeamB`
- **Goalkeepers**: Labeled as `GK <track_id>`
- **Other Objects**: `Ball`, `Main Ref`, `Side Ref`, `Staff`

Each object is drawn with a colored bounding box and label.

For more usage examples and configuration options, see [Usage Guide](docs/USAGE.md).

## 🔧 How It Works

The system uses a **track-level team assignment approach** that provides stable and robust team identification:

### Overview

1. **Detection & Tracking**: YOLOv8 detects objects and assigns stable track IDs
2. **Color Accumulation**: Jersey colors are extracted and accumulated per track over multiple frames
3. **Track-Level Clustering**: Tracks (not individual detections) are clustered into two teams
4. **Stable Assignment**: Team identity remains fixed once assigned

### Detailed Process

#### 1. Object Detection and Tracking
- YOLOv8 performs object detection on each frame
- Tracking assigns stable **track IDs** to players across frames
- Each player maintains the same track_id throughout the video

#### 2. Grass Color Extraction (First Frame)
- Extracts dominant grass color from the first frame
- Used to isolate jersey colors from the background
- HSV color space filtering for accurate grass detection

#### 3. Jersey Color Extraction (Per Frame)
- For each player detection with a valid track_id:
  - Crops player bounding box
  - Removes grass background using HSV filtering
  - Focuses on upper half (jersey area)
  - Extracts average jersey color (BGR)
  - **Accumulates color samples per track_id**

#### 4. Track-Level Color Accumulation
- Each track_id maintains a list of color samples
- Only high-quality detections (bbox area > 500 pixels) are used
- Color samples accumulate continuously over frames

#### 5. Track-Level Clustering
- After sufficient data (30+ frames, 2+ tracks):
  - Computes **one representative color per track** (median)
  - Performs **K-Means clustering (k=2)** on track-level colors
  - Assigns tracks to **TeamA** or **TeamB**
  - Saves K-Means model for new track assignment

#### 6. Team Assignment & Visualization
- **Stable**: Once assigned, team identity remains fixed
- **New Tracks**: Assigned based on color distance to cluster centroids
- **Visualization**: `Player <track_id> | TeamA/TeamB/Unknown`

### Key Advantages

✅ **Stable Team Identity**: Property of track_id, not individual detections  
✅ **Robust to Bad Frames**: One bad frame cannot flip a player's team  
✅ **Camera Independent**: No dependency on x-position or left/right heuristics  
✅ **Accurate**: Uses accumulated color samples for better accuracy  
✅ **Efficient**: Real-time compatible processing  

### Technical Details

- **Tracking**: YOLOv8 tracker with `persist=True` for stable IDs
- **Color Space**: BGR for jersey color representation
- **Clustering**: K-Means (k=2) with median aggregation
- **Minimum Samples**: 3 color samples per track before clustering
- **Frame Threshold**: 30 frames before initial clustering

## 📁 Project Structure

```
Football-Object-Detection/
├── main.py                          # Main application
├── requirements.txt                  # Python dependencies
├── setup.py                         # Package setup
├── README.md                        # This file
├── LICENSE                          # MIT License
├── CONTRIBUTING.md                  # Contribution guidelines
├── CHANGELOG.md                     # Version history
├── PROJECT_STRUCTURE.md             # Detailed structure
├── docs/                            # Documentation
│   ├── INSTALLATION.md              # Installation guide
│   └── USAGE.md                     # Usage guide
├── weights/                         # Model weights (not in git)
│   └── last.pt                      # YOLOv8 weights
├── output/                          # Output videos
└── test_videos/                     # Test videos
```

For detailed structure, see [Project Structure](PROJECT_STRUCTURE.md).

## 📦 Requirements

### Python Packages

- `numpy==1.22.4` - Numerical computing
- `opencv-python==4.6.0.66` - Computer vision
- `scikit-learn==1.3.0` - Machine learning (K-Means)
- `ultralytics==8.0.168` - YOLOv8 detection and tracking

### System Requirements

- **Python**: 3.7 or higher
- **RAM**: 4GB minimum, 8GB+ recommended
- **Storage**: 2GB+ for model weights and dependencies
- **GPU**: Optional but recommended for faster processing

See `requirements.txt` for exact versions.

## 📚 Documentation

- **[Installation Guide](docs/INSTALLATION.md)** - Detailed installation instructions and troubleshooting
- **[Usage Guide](docs/USAGE.md)** - Usage examples, configuration, and performance tips
- **[Contributing](CONTRIBUTING.md)** - Guidelines for contributing to the project
- **[Project Structure](PROJECT_STRUCTURE.md)** - Detailed repository structure
- **[Changelog](CHANGELOG.md)** - Version history and changes

## 🎓 Model Information

### Object Detection Model

- **Framework**: [YOLOv8](https://github.com/ultralytics/ultralytics)
- **Training Dataset**: [SoccerNet Dataset](https://drive.google.com/drive/folders/17w9yhEDZS7gLdZGjiwPQytLz3-iTUpKm)
- **Training Epochs**: 25
- **Classes**: 6 (Player, Goalkeeper, Ball, Main Referee, Side Referee, Staff)

### Detection Classes

- **0** - Player
- **1** - Goalkeeper
- **2** - Ball
- **3** - Main referee
- **4** - Side referee
- **5** - Staff members

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guidelines](CONTRIBUTING.md) for details on:

- Code of conduct
- Development setup
- Pull request process
- Code style guidelines

## 🐛 Troubleshooting

### Common Issues

**Model weights not found**
- Ensure `weights/last.pt` exists in the project root
- Download model weights separately (not included in repo due to size)

**Video won't open**
- Check video path is correct
- Ensure video format is supported (MP4, AVI, MOV)
- Install codec support if needed

**No detections**
- Lower confidence threshold in `main.py`
- Verify model weights are correct
- Check video contains football match footage

**Poor team assignment**
- Ensure sufficient frames are processed (30+)
- Verify players are clearly visible
- Check jersey colors are distinct between teams

For more troubleshooting, see [Installation Guide](docs/INSTALLATION.md).

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [YOLOv8](https://github.com/ultralytics/ultralytics) by Ultralytics
- [SoccerNet Dataset](https://www.soccer-net.org/) for training data
- OpenCV community for computer vision tools

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/Football-Object-Detection/issues)
- **Discussions**: [GitHub Discussions](https://github.com/your-username/Football-Object-Detection/discussions)

## 🔗 Related Projects

- [YOLOv8](https://github.com/ultralytics/ultralytics) - Object detection framework
- [SoccerNet](https://www.soccer-net.org/) - Football video dataset

---

**Made with ⚽ for football analysis**

