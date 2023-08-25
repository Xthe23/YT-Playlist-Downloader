import os
from pytube import YouTube

class DownloadProgress:
    def __init__(self):
        self.previous_percentage = -1
    
    def progress_function(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        percentage = self.percent(size - bytes_remaining, size)
        if percentage != self.previous_percentage:
            progress_bar = self.get_progress_bar(percentage)
            print(f"\r{progress_bar} Downloaded: {percentage:.2f}%", end="", flush=True)
            self.previous_percentage = percentage
    
    def percent(self, bytes_received, total_bytes):
        percentage = (bytes_received / total_bytes) * 100
        return percentage
    
    def get_progress_bar(self, percentage, length=30):
        num_bars = int(percentage / 100 * length)
        progress_bar = "[" + "|" * num_bars + " " * (length - num_bars) + "]"
        return progress_bar

def download_video(video_url, download_path):
    try:
        yt = YouTube(video_url)
        video_stream = yt.streams.get_highest_resolution()
        
        progress_tracker = DownloadProgress()
        yt.register_on_progress_callback(progress_tracker.progress_function)
        
        video_stream.download(output_path=download_path)
        print(f"\nDownloaded: {yt.title}")
    except Exception as e:
        error_message = str(e).lower()
        if "this video is age restricted" in error_message:
            print(f"Skipped age-restricted video: {yt.title}")
        else:
            print(f"Error downloading {yt.title}: {str(e)}")

if __name__ == "__main__":
    video_url = input("What is the video link?\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(script_dir, "Output_video")

    os.makedirs(download_path, exist_ok=True)
    download_video(video_url, download_path)
