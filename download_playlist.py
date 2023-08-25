import os
from pytube import Playlist, YouTube

class DownloadProgress:
    def __init__(self, total_videos):
        self.total_videos = total_videos
        self.successful_downloads = 0
        self.age_restricted_skips = 0
        self.video_titles = []
        self.previous_percentage = -1
    
    def progress_function(self, stream, chunk, bytes_remaining):
        size = stream.filesize
        percentage = self.percent(size - bytes_remaining, size)
        if percentage != self.previous_percentage:
            progress_bar = self.get_progress_bar(percentage)
            title = self.video_titles[0]
            summary = self.get_download_summary(percentage)
            print(f"\r{summary} {progress_bar} {title}", end="", flush=True)
            self.previous_percentage = percentage
    
    def percent(self, bytes_received, total_bytes):
        percentage = (bytes_received / total_bytes) * 100
        return percentage
    
    def get_progress_bar(self, percentage, length=30):
        num_bars = int(percentage / 100 * length)
        progress_bar = "[" + "|" * num_bars + " " * (length - num_bars) + "]"
        return progress_bar
    
    def get_download_summary(self, percentage):
        return f"{percentage:.2f}% Downloaded: {self.successful_downloads}/{self.total_videos} " \
               f"Age-restricted skips: {self.age_restricted_skips}"

def download_playlist(playlist_url, download_path):
    playlist = Playlist(playlist_url)
    total_videos = len(playlist.video_urls)

    os.makedirs(download_path, exist_ok=True)
    
    progress_tracker = DownloadProgress(total_videos)

    for video_url in playlist.video_urls:
        try:
            yt = YouTube(video_url)
            video_stream = yt.streams.get_highest_resolution()
            
            progress_tracker.video_titles.append(yt.title)
            yt.register_on_progress_callback(progress_tracker.progress_function)
            
            video_stream.download(output_path=download_path)
            
            progress_tracker.successful_downloads += 1
            progress_tracker.video_titles.pop(0)  # Remove the used title
            
        except Exception as e:
            error_message = str(e).lower()
            if "this video is age restricted" in error_message:
                progress_tracker.age_restricted_skips += 1
            else:
                print(f"Error downloading {yt.title}: {str(e)}")

    print("\nDownload summary:")
    print(progress_tracker.get_download_summary(100.00))

if __name__ == "__main__":
    playlist_url = input("What is the youtube playlist link?\n")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(script_dir, "Output_playlist")

    download_playlist(playlist_url, download_path)
