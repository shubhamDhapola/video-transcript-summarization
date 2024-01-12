from STT import speech_to_text
from STT import extract_data
from downloader import download_youtube_video
from moviepy.video.tools.subtitles import SubtitlesClip
from moviepy.editor import TextClip, CompositeVideoClip, VideoFileClip

import os
import json
import logging
import sys
from dotenv import load_dotenv
load_dotenv()
logging.basicConfig(level=logging.INFO, stream=sys.stdout)

# change url to your youtube video url
url = "https://www.youtube.com/watch?v=PLiWjL5O2rE"
video_dir = "./video"
subtitle_dir = "./subtitle"

def create_sub(id:str, video_dir:str, subtitle_dir:str)-> None:
    video_path = os.path.join(video_dir, id +'.mp4')
    srt_path = os.path.join(subtitle_dir, id +'.srt')
    main_video = VideoFileClip(video_path)
    generator = lambda txt: TextClip(txt, font="arial", fontsize=50, color="white", bg_color="black",
                                    method='caption', size=(main_video.size[0], 50))

    sub_clip = SubtitlesClip(srt_path, generator).set_position('bottom')
    result = CompositeVideoClip((main_video, sub_clip), size=main_video.size)
    result.write_videofile(f'{video_dir}/{id}_caped.mp4', fps=main_video.fps, temp_audiofile="temp-audio.m4a", 
                            remove_temp=True, codec="libx264", audio_codec="aac")
    logging.info(f"Subtitle Video at {video_dir}/{id}_caped.mp4.")
    return None

def main():
    
    # download youtube video
    title, id = download_youtube_video(url=url, path=video_dir)
    speech_to_text(id=id, video_dir=video_dir, subtitle_dir=subtitle_dir)
    create_sub(id=id, video_dir=video_dir, subtitle_dir=subtitle_dir)
    return None

if __name__ == "__main__":
    main()
