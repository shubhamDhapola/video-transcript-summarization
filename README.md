# YouTube-Speech-to-text-to-subtitle
 create video with subtitle from youtube video
![demo video with subtitle](./video/PZ-GvIOhcf8_caped.mp4)

## How it works
1. download youtube video from a url

2. create srt file from video using deepgram speech to text

3. use moivepy to combine original video and srt file to create video with subtitle

## How to use
1. clone this repo
``` bash
git clone https://github.com/andy3278/YouTube-Speech-to-text-to-subtitle.git
```
2. install dependencies
``` bash
pip install -r requirements.txt
```
3. setup deepgram api key
create a file named .env in the root directory of this repo and add your deepgram api key
``` 
DG_KEY = your deepgram api key
```

4. change the url in main.py to your youtube video url and run main.py
``` python
python main.py
```