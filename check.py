
import torch
from transformers import AutoTokenizer, AutoModelWithLMHead

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
                  
                  
def generate_summary(id:str):
      tokenizer = AutoTokenizer.from_pretrained('t5-base')
      model = AutoModelWithLMHead.from_pretrained('t5-base', return_dict=True)

      # Example usage:
      input_file = 'input.srt'
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
      
