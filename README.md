# Audio Transcription with Whisper

This project uses OpenAI's Whisper model to transcribe audio files. It slices audio into chunks, processes each with Whisper, and concatenates the results.

## Features
- Support for M4A and WAV files
- Auto-slicing of audio for improved processing
- Fallback to smaller models if needed
- Saves transcription to a text file and prints to terminal

## Usage
- Install required packages: `ffmpeg`, `tqdm`, and `whisper`.
- Place audio files in the same directory.
- Run the script with `python transcribe.py`.

## Requirements
- Python 3.7+
- ffmpeg
- tqdm
- openai-whisper
