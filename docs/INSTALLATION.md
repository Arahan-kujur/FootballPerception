# Installation Guide

## Prerequisites

- Python 3.7 or higher
- pip (Python package manager)
- Git (for cloning the repository)

## Step-by-Step Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/Football-Object-Detection.git
cd Football-Object-Detection
```

### 2. Create a Virtual Environment (Recommended)

**Using venv:**
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

**Using conda:**
```bash
conda create -n football-detection python=3.9
conda activate football-detection
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Download Model Weights

The model weights are not included in the repository due to their size. You need to:

1. Download the trained YOLOv8 weights
2. Place them in the `weights/` directory
3. Ensure the file is named `last.pt` (or update the path in `main.py`)

**Note:** The weights should be trained on the SoccerNet dataset with 6 classes:
- Player
- Goalkeeper
- Ball
- Main Referee
- Side Referee
- Staff

### 5. Verify Installation

Test the installation by checking if all dependencies are installed:

```bash
python -c "import cv2, numpy, ultralytics, sklearn; print('All dependencies installed!')"
```

## Troubleshooting

### Common Issues

**Issue: ModuleNotFoundError**
- Solution: Ensure your virtual environment is activated and dependencies are installed

**Issue: CUDA/GPU errors**
- Solution: Install PyTorch with CUDA support if using GPU, or use CPU-only version

**Issue: Model weights not found**
- Solution: Ensure `weights/last.pt` exists in the project root

**Issue: Video codec errors**
- Solution: Install ffmpeg: `conda install ffmpeg` or download from https://ffmpeg.org/

## Optional: Development Setup

For development, you may want to install additional tools:

```bash
pip install pytest black flake8 mypy
```

## System Requirements

- **Minimum RAM:** 4GB
- **Recommended RAM:** 8GB+
- **Storage:** 2GB+ for model weights and dependencies
- **GPU:** Optional but recommended for faster processing

