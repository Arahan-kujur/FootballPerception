# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-XX-XX

### Added
- Track-level team assignment system
- YOLOv8 object detection and tracking integration
- Jersey color extraction and accumulation per track
- K-Means clustering for track-level team classification
- Stable team identity assignment (TeamA/TeamB)
- Support for processing football match videos
- Comprehensive documentation and README

### Changed
- Migrated from per-frame team assignment to track-level assignment
- Removed left/right positioning-based team logic
- Updated to use track IDs for stable player identification
- Improved team assignment robustness and accuracy

### Technical Details
- Uses YOLOv8 tracking with persistent track IDs
- Accumulates jersey color samples over multiple frames
- Performs clustering on track-level color vectors (not per-detection)
- Assigns teams as TeamA/TeamB (no longer Player-L/Player-R)

