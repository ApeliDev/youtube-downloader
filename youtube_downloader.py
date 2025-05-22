import yt_dlp
import os
import sys
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, download_path="./downloads"):
        """
        Initialize the YouTube downloader
        
        Args:
            download_path (str): Directory to save downloaded videos
        """
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
        # Configure yt-dlp options for high quality
        self.ydl_opts = {
            'format': 'best[height<=1080]',  # Best quality up to 1080p
            'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
            'ignoreerrors': True,
            'no_warnings': False,
        }
    
    def download_video(self, url, quality='best'):
        """
        Download a single video
        
        Args:
            url (str): YouTube video URL
            quality (str): Video quality preference
        """
        # Quality options
        quality_formats = {
            'best': 'best',
            '1080p': 'best[height<=1080]',
            '720p': 'best[height<=720]',
            '480p': 'best[height<=480]',
            'audio_only': 'bestaudio/best'
        }
        
        # Update format based on quality preference
        self.ydl_opts['format'] = quality_formats.get(quality, 'best')
        
        try:
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                print(f"Downloading: {url}")
                ydl.download([url])
                print("Download completed successfully!")
                
        except Exception as e:
            print(f"Error downloading video: {e}")
    
    def download_playlist(self, playlist_url, quality='best'):
        """
        Download entire playlist
        
        Args:
            playlist_url (str): YouTube playlist URL
            quality (str): Video quality preference
        """
        quality_formats = {
            'best': 'best',
            '1080p': 'best[height<=1080]',
            '720p': 'best[height<=720]',
            '480p': 'best[height<=480]',
            'audio_only': 'bestaudio/best'
        }
        
        playlist_opts = self.ydl_opts.copy()
        playlist_opts['format'] = quality_formats.get(quality, 'best')
        playlist_opts['outtmpl'] = str(self.download_path / '%(playlist)s/%(title)s.%(ext)s')
        
        try:
            with yt_dlp.YoutubeDL(playlist_opts) as ydl:
                print(f"Downloading playlist: {playlist_url}")
                ydl.download([playlist_url])
                print("Playlist download completed!")
                
        except Exception as e:
            print(f"Error downloading playlist: {e}")
    
    def get_video_info(self, url):
        """
        Get video information without downloading
        
        Args:
            url (str): YouTube video URL
        """
        try:
            with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
                info = ydl.extract_info(url, download=False)
                
                print(f"Title: {info.get('title', 'N/A')}")
                print(f"Duration: {info.get('duration', 'N/A')} seconds")
                print(f"View Count: {info.get('view_count', 'N/A')}")
                print(f"Upload Date: {info.get('upload_date', 'N/A')}")
                print(f"Channel: {info.get('uploader', 'N/A')}")
                
                # Available formats
                if 'formats' in info:
                    print("\nAvailable formats:")
                    for fmt in info['formats'][-5:]:  # Show last 5 formats
                        height = fmt.get('height', 'audio')
                        ext = fmt.get('ext', 'unknown')
                        filesize = fmt.get('filesize')
                        size_mb = f"{filesize / (1024*1024):.1f}MB" if filesize else "Unknown size"
                        print(f"  {height}p {ext} - {size_mb}")
                        
        except Exception as e:
            print(f"Error getting video info: {e}")

def main():
    """Main function with interactive menu"""
    downloader = YouTubeDownloader()
    
    while True:
        print("\n" + "="*50)
        print("YouTube Video Downloader")
        print("="*50)
        print("1. Download single video")
        print("2. Download playlist")
        print("3. Get video information")
        print("4. Change download directory")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == '1':
            url = input("Enter YouTube video URL: ").strip()
            if url:
                print("\nQuality options:")
                print("1. Best available")
                print("2. 1080p")
                print("3. 720p") 
                print("4. 480p")
                print("5. Audio only")
                
                quality_choice = input("Select quality (1-5): ").strip()
                quality_map = {'1': 'best', '2': '1080p', '3': '720p', '4': '480p', '5': 'audio_only'}
                quality = quality_map.get(quality_choice, 'best')
                
                downloader.download_video(url, quality)
            else:
                print("Invalid URL!")
        
        elif choice == '2':
            url = input("Enter YouTube playlist URL: ").strip()
            if url:
                print("\nQuality options:")
                print("1. Best available")
                print("2. 1080p")
                print("3. 720p")
                print("4. 480p")
                print("5. Audio only")
                
                quality_choice = input("Select quality (1-5): ").strip()
                quality_map = {'1': 'best', '2': '1080p', '3': '720p', '4': '480p', '5': 'audio_only'}
                quality = quality_map.get(quality_choice, 'best')
                
                downloader.download_playlist(url, quality)
            else:
                print("Invalid URL!")
        
        elif choice == '3':
            url = input("Enter YouTube video URL: ").strip()
            if url:
                downloader.get_video_info(url)
            else:
                print("Invalid URL!")
        
        elif choice == '4':
            new_path = input("Enter new download directory: ").strip()
            if new_path:
                downloader = YouTubeDownloader(new_path)
                print(f"Download directory changed to: {new_path}")
        
        elif choice == '5':
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice! Please enter 1-5.")

if __name__ == "__main__":
    # Check if yt-dlp is installed
    try:
        import yt_dlp
    except ImportError:
        print("Error: yt-dlp is not installed!")
        print("Please install it using: pip install yt-dlp")
        sys.exit(1)
    
    main()