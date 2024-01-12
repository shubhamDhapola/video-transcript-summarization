from pytube import YouTube
from pytube import extract
import logging
import sys

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

def download_youtube_video(url:str, path:str ,file_type='mp4')-> tuple[str, str]:
    yt = YouTube(url)
    stream = yt.streams.first()
    logging.info(f"Downloading {yt.title}...")
    id = extract.video_id(url)
    yt.streams.filter(progressive=True, file_extension=file_type).order_by('resolution').desc().first().download(output_path=path, filename=id+".mp4")

    logging.info(f"Video id: {id} download complete.")
    return yt.title, id