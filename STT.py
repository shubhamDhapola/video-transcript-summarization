import os
import json
import logging
import sys
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead
from deepgram import DeepgramClient, DeepgramClientOptions, PrerecordedOptions
from deepgram_captions import DeepgramConverter, srt
from dotenv import load_dotenv

from downloader import download_youtube_video

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
load_dotenv()

dg_key = os.getenv("DG_KEY")

# extract data from deepgram json like response
def extract_data(response):
    data = {
        "metadata": {
            "transaction_key": response.metadata.transaction_key,
            "request_id": response.metadata.request_id,
            "sha256": response.metadata.sha256,
            "created": response.metadata.created,
            "duration": response.metadata.duration,
            "channels": response.metadata.channels,
            "models": response.metadata.models,
            "model_info": {k: vars(v) for k, v in response.metadata.model_info.items()},
        },
        "results": {
            "channels": [
                {
                    "alternatives": [
                        {
                            "transcript": alt.transcript,
                            "confidence": alt.confidence,
                            "words": [vars(word) for word in alt.words],
                        }
                        for alt in channel.alternatives
                    ]
                }
                for channel in response.results.channels
            ]
        },
    }
    return data

def speech_to_text(id : str, video_dir : str, subtitle_dir: str)-> None:
    # initalize deepgram client
    deepgram = DeepgramClient(dg_key)

    # get video path
    video_path = os.path.join(video_dir, id +'.mp4')

    # open mp4 file and call deepgram api
    options = PrerecordedOptions(
            model="nova-2", # or enhanced
            smart_format=True,
        )
    with open(video_path, 'rb') as f:
        data = f.read()
        url_response = deepgram.listen.prerecorded.v("1").transcribe_file({'buffer': data}, options)
    logging.info(f"Transcription complete.")

    # save data as json file
    data = extract_data(url_response)
    with open(f'{subtitle_dir}/{id}.json', 'w') as f:
        json.dump(data, f, indent=4)
    json_file_path = os.path.join(subtitle_dir, id +'.json')

    # convert json file to srt file
    with open(json_file_path, "r") as json_file:
        dg_transcription = json.load(json_file)
    transcription = DeepgramConverter(dg_transcription)
    captions = srt(transcription)
    logging.info(f"Captioning complete. \n store as {id}.srt")
    with open(f'{subtitle_dir}/{id}.srt', 'w') as f:
        f.write(captions)

    # return none because downloader already return title and id
    return None





def convert_srt_to_double_quotes(input_file, output_file):
            with open(input_file, 'r') as f:
                  srt_content = f.read()

            # Split the content into individual subtitle blocks
            subtitle_blocks = srt_content.strip().split('\n\n')

            # Process each subtitle block
            modified_lines = []
            for block in subtitle_blocks:
                  lines = block.split('\n')
                  if len(lines) >= 3:  # Ensure it's a valid subtitle block
                        # Extract the main line of text
                        main_line = lines[2]
                        # Enclose the main line in double inverted commas
                        main_line_with_quotes =  main_line
                        modified_lines.append(main_line_with_quotes)

            # Join the modified lines back together
            modified_srt_content = '\n'.join(modified_lines)

            # Write the modified content to the output file
            with open(output_file, 'w') as f:
                  f.write(modified_srt_content)
                  
                  
def generate_summary(id:str, subtitle_dir:str):
      tokenizer = AutoTokenizer.from_pretrained('t5-base')
      model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

      # Example usage:
      input_file = f'{subtitle_dir}/{id}.srt'
      output_file = 'output.txt'
      convert_srt_to_double_quotes(input_file, output_file)


      with open('output.txt', 'r') as file:
            sequence = file.read()
      

      inputs = tokenizer.encode("summarize: " + sequence,
                              return_tensors='pt',
                              max_length=512,
                              truncation=True)

      summary_ids = model.generate(inputs, max_length=150, min_length=80, length_penalty=5., num_beams=2)

      summary = tokenizer.decode(summary_ids[0])

      print(summary)
      
