# RealSense Camera Viewer

Python applications to view Intel RealSense camera feeds.

## Files

- `intel-realsense.py` - Full viewer with RGB and Depth streams side-by-side
- `requirements.txt` - Python dependencies

## Installation

### 1. Install Python dependencies

```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install pyrealsense2 opencv-python numpy
```

### 2. Install RealSense SDK (if not already installed)

## Usage

### Simple RGB Viewer
```bash
python intel-realsense.py
```
- Shows only the RGB camera feed
- Press 'q' to quit

### Full RGB + Depth Viewer
```bash
python intel-realsense.py
```
- Shows RGB camera on left, depth map on right
- Displays distance measurement at center point
- Press 'q' to quit
- Press 's' to save snapshot

## Features

### intel-realsense.py
- Side-by-side RGB and Depth visualization
- Real-time distance measurement at center point
- Colorized depth map (JET colormap)
- Snapshot capture (press 's')
- Frame alignment for accurate depth overlay

### intel-realsense.py.py
- Lightweight RGB-only viewer
- Minimal dependencies
- Fast and simple

## Requirements

- Intel RealSense camera (D400 series recommended)
- USB 3.0 port
- Python 3.6+
- librealsense2 SDK

## Notes

- The beta version of pyrealsense2 may have additional features
- For production use, consider using the stable version: `pip install pyrealsense2`
- Default resolution is 640x480 @ 30fps (can be modified in code)
