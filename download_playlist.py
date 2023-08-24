import os
from pytube import Playlist, YouTube


def download_playlist(playlist_url, download_path):
    playlist = Playlist(playlist_url)
    total_videos = len(playlist.video_urls)
    successful_downloads = 0
    age_restricted_skips = 0

    for video_url in playlist.video_urls:
        try:
            yt = YouTube(video_url)
            yt.streams.get_highest_resolution().download(output_path=download_path)
            print(f"Downloaded: {yt.title}")
            successful_downloads += 1
        except Exception as e:
            error_message = str(e).lower()
            if "this video is age restricted" in error_message:
                age_restricted_skips += 1
                print(f"Skipped age-restricted video: {yt.title}")
            else:
                print(f"Error downloading {yt.title}: {str(e)}")

    print("\nDownload summary:")
    print(f"Total videos in playlist: {total_videos}")
    print(f"Successful downloads: {successful_downloads}")
    print(f"Age-restricted videos skipped: {age_restricted_skips}")
    print("\n")


if __name__ == "__main__":
    playlist_url = input("What is the playlist link?")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    download_path = os.path.join(script_dir, "Output_playlist")

    download_playlist(playlist_url, download_path)
