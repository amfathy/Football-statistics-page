# upload.py

import cv2
import os
import shutil

def clear_output_dir(output_dir):
    """
    Clears the output directory before saving frames.
    """
    if os.path.exists(output_dir):
        shutil.rmtree(output_dir)  
    os.makedirs(output_dir, exist_ok=True)  

def save_frames_from_video(video_path, output_dir, interval_sec):
    try:
        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print(f"Error: Could not open video file {video_path}")
            return

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            print("Error: Could not retrieve FPS. The video might have variable frame rates.")
            return

        print(f"Frame rate: {fps} fps")

        frame_interval = int(fps * interval_sec)
        print(f"Frame interval: {frame_interval} frames")

        clear_output_dir(output_dir)  

        frame_count = 0
        saved_frame_count = 0

        while True:
            ret, frame = cap.read()

            if not ret:
                break

            if frame_count % frame_interval == 0:
                frame_filename = os.path.join(output_dir, f"frame_{saved_frame_count:05d}.jpg")
                cv2.imwrite(frame_filename, frame)
                print(f"Saved {frame_filename}")
                saved_frame_count += 1

            frame_count += 1

        cap.release()
        print(f"Total frames saved: {saved_frame_count}")
    
    except Exception as e:
        print(f"An error occurred: {e}")

def Upload_main():
     
     video_path = r'D:\college\GP\phase2\video_dividing/Untitled video - Made with Clipchamp.mp4'
     output_dir = r'D:\college\GP\phase2\video_dividing\frames'
     interval_sec = 1.35
     save_frames_from_video(video_path, output_dir, interval_sec)

if __name__ == "__main__":
     Upload_main()
