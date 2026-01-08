#!/usr/bin/env python3
"""
RealSense Camera Viewer
Displays RGB and Depth streams from Intel RealSense camera
"""

import pyrealsense2 as rs
import numpy as np
import cv2

def main():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    
    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    
    print("Camera device found:")
    print(f"  Name: {device.get_info(rs.camera_info.name)}")
    print(f"  Serial Number: {device.get_info(rs.camera_info.serial_number)}")
    print(f"  Firmware Version: {device.get_info(rs.camera_info.firmware_version)}")
    
    # Enable streams
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    
    # Start streaming
    print("\nStarting camera streams...")
    pipeline.start(config)
    
    # Create alignment object to align depth to color
    align_to = rs.stream.color
    align = rs.align(align_to)
    
    print("Camera started! Press 'q' to quit, 's' to save snapshot")
    
    try:
        while True:
            # Wait for a coherent pair of frames: depth and color
            frames = pipeline.wait_for_frames()
            
            # Align the depth frame to color frame
            aligned_frames = align.process(frames)
            
            # Get aligned frames
            depth_frame = aligned_frames.get_depth_frame()
            color_frame = aligned_frames.get_color_frame()
            
            if not depth_frame or not color_frame:
                continue
            
            # Convert images to numpy arrays
            depth_image = np.asanyarray(depth_frame.get_data())
            color_image = np.asanyarray(color_frame.get_data())
            
            # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
            # Invert the depth values so closer = red, farther = blue
            depth_8bit = cv2.convertScaleAbs(depth_image, alpha=0.03)
            depth_inverted = 255 - depth_8bit  # Invert the values
            depth_colormap = cv2.applyColorMap(depth_inverted, cv2.COLORMAP_JET)
            
            # Get depth scale
            depth_sensor = pipeline_profile.get_device().first_depth_sensor()
            depth_scale = depth_sensor.get_depth_scale()
            
            # Add distance info at center of image
            height, width = depth_image.shape
            center_x, center_y = width // 2, height // 2
            distance = depth_frame.get_distance(center_x, center_y)
            
            # Add text overlay on color image
            cv2.circle(color_image, (center_x, center_y), 5, (0, 255, 0), -1)
            cv2.putText(
                color_image, 
                f"Distance: {distance:.2f}m", 
                (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1, 
                (0, 255, 0), 
                2
            )
            
            # Stack images horizontally
            images = np.hstack((color_image, depth_colormap))
            
            # Add labels
            cv2.putText(
                images, 
                "RGB Camera", 
                (10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (255, 255, 255), 
                2
            )
            cv2.putText(
                images, 
                "Depth Map", 
                (width + 10, 60), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                0.7, 
                (255, 255, 255), 
                2
            )
            
            # Show images
            cv2.imshow('RealSense Camera Viewer - RGB & Depth', images)
            
            # Handle keyboard input
            key = cv2.waitKey(1)
            if key & 0xFF == ord('q'):
                print("\nQuitting...")
                break
            elif key & 0xFF == ord('s'):
                # Save snapshot
                cv2.imwrite('realsense_rgb.png', color_image)
                cv2.imwrite('realsense_depth.png', depth_colormap)
                print("Snapshot saved!")
                
    finally:
        # Stop streaming
        pipeline.stop()
        cv2.destroyAllWindows()
        print("Camera stopped.")

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure:")
        print("  1. RealSense camera is connected")
        print("  2. You have installed: pip install pyrealsense2")
        print("  3. You have installed: pip install opencv-python")