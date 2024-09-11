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

# Function to extract frames from the downloaded video with frame skipping
def extract_frames_from_video(video_path, output_folder, frame_skip=30):
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
            frame_filename = os.path.join(output_folder, f"frame_{saved_frame_count:04d}.jpg")
            cv2.imwrite(frame_filename, frame)
            saved_frame_count += 1
        frame_number += 1

    video.release()
    print(f"Extracted {saved_frame_count} frames, skipping every {frame_skip} frames.")

# Main function to download video and extract frames with frame skipping
def download_and_extract_frames(youtube_url, output_folder, frame_skip=30):
    print("Downloading video...")
    video_path = download_youtube_video(youtube_url, output_folder)
    print(f"Video downloaded. Extracting frames now...")
    extract_frames_from_video(video_path, output_folder, frame_skip)

# Example usage
youtube_url = "https://youtu.be/Rhvy2AWkxY8"
output_folder = "Goals"
frame_skip = 10  # Save one frame every 30 frames (approximately 1 frame per second for a 30 fps video)
download_and_extract_frames(youtube_url, output_folder, frame_skip)
