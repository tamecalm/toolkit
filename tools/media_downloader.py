import os
import sys
import logging
from pytube import YouTube

# Configure logging
logging.basicConfig(
    filename="media_downloader.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def download_media(url):
    try:
        yt = YouTube(url)
        
        logging.info(f"Fetching media: {yt.title} by {yt.author}")
        print(f"Title: {yt.title}")
        print("Choose download type:")
        print("1. Video")
        print("2. Audio")
        
        choice = input("Enter your choice (1 or 2): ")

        if choice == "1":
            stream = yt.streams.filter(progressive=True, file_extension="mp4").get_highest_resolution()
            logging.info("Downloading video...")
        elif choice == "2":
            stream = yt.streams.filter(only_audio=True).first()
            logging.info("Downloading audio...")
        else:
            print("Invalid choice. Exiting.")
            logging.warning("Invalid download choice made.")
            return

        output_path = stream.download()
        logging.info(f"Downloaded successfully to {output_path}")
        print(f"Downloaded successfully to {output_path}")

    except Exception as e:
        logging.error(f"An error occurred: {e}")
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    url = input("Enter the YouTube URL: ")
    download_media(url)
