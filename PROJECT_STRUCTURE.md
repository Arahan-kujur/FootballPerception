# Project Structure

```
Football-Object-Detection/
│
├── main.py                          # Main application entry point
├── requirements.txt                  # Python dependencies
├── setup.py                         # Package setup configuration
│
├── README.md                        # Main project documentation
├── LICENSE                          # MIT License
├── CONTRIBUTING.md                  # Contribution guidelines
├── CHANGELOG.md                     # Version history
├── PROJECT_STRUCTURE.md             # This file
│
├── .gitignore                       # Git ignore rules
├── .gitattributes                   # Git attributes for line endings
│
├── docs/                            # Documentation directory
│   ├── INSTALLATION.md              # Installation guide
│   └── USAGE.md                     # Usage guide
│
├── weights/                         # Model weights directory
│   ├── .gitkeep                    # Keep directory in git
│   ├── last.pt                     # YOLOv8 model weights (not in git)
│   └── best.pt                      # Best model weights (not in git)
│
├── output/                          # Output videos directory
│   ├── .gitkeep                    # Keep directory in git
│   └── *.mp4                       # Processed videos (not in git)
│
├── test_videos/                     # Test video files
│   ├── .gitkeep                    # Keep directory in git
│   └── *.mp4                       # Test videos (not in git)
│
└── Football_Object_Detection.ipynb  # Jupyter notebook with examples
```

## Directory Descriptions

### Root Files

- **main.py**: Main application script with video processing logic
- **requirements.txt**: Python package dependencies
- **setup.py**: Package installation configuration

### Documentation

- **README.md**: Main project overview and quick start guide
- **docs/INSTALLATION.md**: Detailed installation instructions
- **docs/USAGE.md**: Usage guide and configuration options
- **CONTRIBUTING.md**: Guidelines for contributors
- **CHANGELOG.md**: Version history and changes

### Directories

- **weights/**: Contains YOLOv8 model weights (excluded from git due to size)
- **output/**: Output directory for processed videos
- **test_videos/**: Sample videos for testing
- **docs/**: Additional documentation files

## File Size Considerations

The following files/directories are excluded from git via `.gitignore`:

- **weights/*.pt**: Model weights (typically 50-200MB)
- **output/*.mp4**: Processed videos (can be large)
- **test_videos/*.mp4**: Test videos (can be large)

Users should download model weights separately and place them in the `weights/` directory.

## Adding New Files

When adding new files:

1. **Code files**: Place in root or appropriate subdirectory
2. **Documentation**: Add to `docs/` directory
3. **Tests**: Create a `tests/` directory if needed
4. **Examples**: Add example scripts to root or `examples/` directory

