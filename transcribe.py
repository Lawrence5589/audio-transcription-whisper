import os
import whisper
from tqdm import tqdm
import subprocess

# Function to slice audio into chunks
def slice_audio(input_file, chunk_length=60):  # chunk_length in seconds
    base_name = os.path.basename(input_file).split('.')[0]
    output_files = []

    cmd = [
        'ffmpeg',
        '-i', input_file,
        '-f', 'segment',
        '-segment_time', str(chunk_length),
        '-c:a', 'pcm_s16le',
        '-ar', '16000',
        '-ac', '1',
        f'{base_name}_%03d.wav'
    ]

    subprocess.run(cmd, check=True)

    # Verify and collect chunk files
    for i in range(1000):  # Arbitrary large number to check all possible chunks
        chunk_name = f'{base_name}_{i:03d}.wav'
        if os.path.exists(chunk_name):
            output_files.append(chunk_name)

    print("Found chunks:", output_files)
    return sorted(output_files)

# Load Whisper model
model = whisper.load_model("base")

# Transcription with progress
def transcribe_audio(input_file):
    try:
        chunks = slice_audio(input_file)
        
        if not chunks:
            print("No chunks were created. Check the slicing process.")
            return ""

        full_transcription = ""

        for chunk in tqdm(chunks, desc="Transcribing"):
            try:
                print(f"Processing {chunk}")
                result = model.transcribe(chunk)
                transcription = result.get('text', "")
                print(f"Transcription for {chunk}: {transcription}")
                full_transcription += transcription + " "
            except Exception as e:
                print(f"Error transcribing {chunk}: {e}")
                
            os.remove(chunk)  # Remove chunk after processing

        print("Final transcription:", full_transcription)
        return full_transcription
    except Exception as e:
        print(f"An error occurred: {e}")
        return ""

# Specify path to your audio file
audio_file = " "

# Transcribe
transcript = transcribe_audio(audio_file)

# Save transcription with UTF-8 encoding
if transcript:
    with open("transcription.txt", "w", encoding="utf-8") as file:
        file.write(transcript)
    print("Transcription complete!")
else:
    print("No transcription was performed.")