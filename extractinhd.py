import cv2
import os
import yt_dlp

# Function to download video using yt-dlp
def download_youtube_video(youtube_url, output_path):
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': os.path.join(output_path, 'downloaded_video.mp4'),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([youtube_url])

    return os.path.join(output_path, 'downloaded_video.mp4')

# Function to extract and resize frames to 1920x1080
def extract_frames_from_video(video_path, output_folder, frame_skip=30, resize_dim=(1920, 1080)):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    video = cv2.VideoCapture(video_path)
    frame_number = 0
    saved_frame_count = 0

    while True:
        success, frame = video.read()
        if not success:
            break
        if frame_number % frame_skip == 0:
            # Resize the frame to 1920x1080
            resized_frame = cv2.resize(frame, resize_dim)
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, resized_frame)
            saved_frame_count += 1
        frame_number += 1

    video.release()
    print(f"Extracted {saved_frame_count} frames, skipping every {frame_skip} frames, and resized them to {resize_dim[0]}x{resize_dim[1]}.")

# Main function to download video and extract resized frames
def download_and_extract_frames(youtube_url, output_folder, frame_skip=30, resize_dim=(1920, 1080)):
    print("Downloading video...")
    video_path = download_youtube_video(youtube_url, output_folder)
    print(f"Video downloaded. Extracting and resizing frames now...")
    extract_frames_from_video(video_path, output_folder, frame_skip, resize_dim)

# Example usage
youtube_url = "https://youtu.be/bQv9RgP7Ys4"
output_folder = "trackling"
frame_skip = 30  # Save one frame every 30 frames (approximately 1 frame per second for a 30 fps video)
resize_dim = (1920, 1080)  # Resize all frames to 1920x1080

download_and_extract_frames(youtube_url, output_folder, frame_skip, resize_dim)
