# README for Quran Video Creator

## Overview

The **Quran Video Creator** is a Python-based application designed to create videos from Quranic text and audio. It fetches Quranic text and audio for a specific page from an online API, generates images with the text, and combines them with the audio to produce a video. The background image is used as the backdrop for the video.

## Features

- Fetches Quranic text and audio from an API.
- Creates images with Quranic text using Arabic text shaping and bidirectional text rendering.
- Downloads audio files and synchronizes them with text images.
- Produces a video with customizable background and audio.

## Requirements

- Python 3.x
- Libraries:
  - `requests`
  - `moviepy`
  - `PIL` (Pillow)
  - `arabic_reshaper`
  - `bidi`
- Font file: `NotoSansArabic-Bold.ttf`
- Background image: `background.jpg`
- FFmpeg: Ensure that FFmpeg is installed and accessible in your system's PATH.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone <repository_url>
   cd <repository_directory>
   ```

2. **Install Python Dependencies:**
   Create a virtual environment and install required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install requests moviepy Pillow arabic_reshaper bidi
   ```

3. **Download Required Font:**
   Ensure that the `NotoSansArabic-Bold.ttf` font file is available in the `Fonts` directory. You can download it from Google Fonts or similar sources.

4. **Install FFmpeg:**
   - **Windows:** Download from [FFmpeg](https://ffmpeg.org/download.html) and add to PATH.
   - **macOS:** Install via Homebrew:
     ```bash
     brew install ffmpeg
     ```
   - **Linux:** Install via package manager (e.g., `sudo apt-get install ffmpeg`).

## Usage

1. **Run the Script:**
   Execute the script to create a video for a specific Quran page:

   ```bash
   python quran_video_creator.py
   ```

2. **Input Page Number:**
   When prompted, enter the desired Quran page number.

3. **Output:**
   The script will create a video file named `quran_page_<page_number>_video.mp4` in the current directory.

## Troubleshooting

### Known Issues

1. **Video Creation Time:**

- It takes a long time to make a video, it takes between 5 to 20 min to generate a video for a page from quran, it depends on the number of ayahs.

2. **Silence Between Ayahs:**

- There is some small silence between each ayah, this silence is originated from the api audio itself.

3. **Text Formatting:**

- The text formatting isn't perfect, the order of words is correct , but lines distribution and tachkil are missing.

## Log File

The application generates a log file named `quran_video_creator.log` in the same directory. Check this file for detailed logs and error messages if you encounter issues.
