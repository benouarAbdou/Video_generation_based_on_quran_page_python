from math import floor
import requests
import os
import logging
from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import arabic_reshaper
from bidi.algorithm import get_display
import datetime
import bidi.algorithm

# Set up logging
logging.basicConfig(filename='quran_video_creator.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def fetch_quran_page(page_number):
    try:
        # Fetch text
        text_api_url = f"https://api.alquran.cloud/v1/page/{page_number}/quran-simple"
        text_response = requests.get(text_api_url)
        text_response.raise_for_status()
        text_data = text_response.json()

        # Fetch audio
        audio_api_url = f"https://api.alquran.cloud/v1/page/{page_number}/ar.abdurrahmaansudais"
        audio_response = requests.get(audio_api_url)
        audio_response.raise_for_status()
        audio_data = audio_response.json()

        # Extract text and audio URLs
        text_ayahs = text_data['data']['ayahs']
        audio_ayahs = audio_data['data']['ayahs']

        texts = [ayah['text'] + f" ﴿{ayah['numberInSurah']}﴾" for ayah in text_ayahs]
        audio_urls = [ayah['audio'] for ayah in audio_ayahs]

        # Ensure texts and audio_urls have the same length
        if len(texts) != len(audio_urls):
            raise ValueError("Mismatch between number of text ayahs and audio ayahs")

        # Modify texts
        modified_texts = []
        for ayah in text_ayahs:
            text = ayah['text']
            number_in_surah = ayah['numberInSurah']
            words = text.split()
            
            if number_in_surah == 1:
                
                new_text = "" + ' '.join(words[4:])
                
            else:
                new_text = text
            
            modified_texts.append(new_text + f" ﴿{number_in_surah}﴾")

        return modified_texts, audio_urls
    except Exception as e:
        logging.error(f"Error fetching Quran page: {str(e)}")
        raise

def create_text_image(text, size=(1280, 1280)):
    try:
        image = Image.new('RGBA', size, (0, 0, 0, 0))  # Transparent background
        draw = ImageDraw.Draw(image)
        font = ImageFont.truetype("Fonts/NotoSansArabic-Bold.ttf", 100)  # Increase font size
        
        # Reshape and bidi the text
        reshaped_text = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped_text)
        
        # Wrap text and center it
        lines = []
        line = ""
        words = bidi_text.split()
        for word in words:
            if draw.textbbox((0, 0), line + word, font=font)[2] <= size[0] - 20:
                line += word + " "
            else:
                lines.append(line)
                line = word + " "
        lines.append(line)
        
        # Reverse the lines to fix the vertical text reversal issue
        lines = lines[::-1]
        
        y_text = (size[1] - len(lines) * 80) // 2  # Increase spacing
        for line in lines:
            width, height = draw.textbbox((0, 0), line, font=font)[2:]
            draw.text(((size[0] - width) / 2, y_text), line, font=font, fill='white')
            y_text += 120  # Increase line spacing

        return image
    except Exception as e:
        logging.error(f"Error creating text image: {str(e)}")
        raise

def create_video(page_number, background_image_path, output_path):
    try:
        # Fetch Quran page data
        texts, audio_urls = fetch_quran_page(page_number)
        logging.info(f"Fetched data for page {page_number}")
        
        clips = []
        
        for i, (text, audio_url) in enumerate(zip(texts, audio_urls)):
            # Create text image
            text_image = create_text_image(text)
            text_image_path = f"temp_text_image_{page_number}_{i}.png"
            text_image.save(text_image_path)
            logging.info(f"Created text image: {text_image_path}")
            
            # Download audio file
            audio_response = requests.get(audio_url)
            audio_response.raise_for_status()
            audio_file = f"temp_audio_{page_number}_{i}.mp3"
            with open(audio_file, 'wb') as f:
                f.write(audio_response.content)
            logging.info(f"Downloaded audio: {audio_file}")
            
            # Load audio to get its duration
            audio = AudioFileClip(audio_file)
            duration = audio.duration
            
            # Load video clips
            background_clip = ImageClip(background_image_path).set_duration(duration)
            text_clip = ImageClip(text_image_path).set_duration(duration)
            
            # Compose video
            video = CompositeVideoClip([background_clip, text_clip.set_position('center')]).set_duration(duration)
            
            # Add audio
            final_clip = video.set_audio(audio)
            clips.append(final_clip)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Write video file
        final_video.write_videofile(output_path, fps=10,threads=16,  audio_codec='aac',logger=None,codec="libx264",preset="medium",ffmpeg_params=['-b:v','10000k'],)
        logging.info(f"Video created: {output_path}")
        
        # Clean up temporary files
        for i in range(len(texts)):
            os.remove(f"temp_text_image_{page_number}_{i}.png")
            os.remove(f"temp_audio_{page_number}_{i}.mp3")
        logging.info("Temporary files cleaned up")
    except Exception as e:
        logging.error(f"Error creating video: {str(e)}")
        raise

'''def getAR(arWord, w_w=0, f_w=0):
    arWord = arWord.strip()
    if len(arWord) <= 0: return ''
    startList0 = bidi.algorithm.get_display(arabic_reshaper.reshape(arWord))
    if (not w_w) or (not f_w):
        return startList0
    else:
        # return startList0
        startList = startList0.split(' ')[::-1]
        if len(startList) == 0: return ''
        if len(startList) == 1: return str(startList[0])
        n = floor( w_w / f_w )
        for i in startList:
            if len(i) > n: return startList0
        tempS = ''
        resultList = []
        for i in range(0, len(startList)):
            if (tempS != ''): tempS = ' ' + tempS
            if (len(tempS) + (len(startList[i])) > n):
                tempS = tempS + "\n"
                resultList.append(tempS)
                tempS = startList[i]
            else:
                tempS = startList[i] + tempS
                if i == (len(startList)-1):
                    resultList.append(tempS)
        return ''.join(resultList)'''
# Usage
try:
    now = datetime.datetime.now()
    print(now.strftime("%H:%M:%S"))
    page_number = input("Enter the Quran page number: ")
    background_image_path = "background.jpg"
    output_path = f"quran_page_{page_number}_video.mp4"
    
    create_video(page_number, background_image_path, output_path)
    print(f"Video created: {output_path}")
    now = datetime.datetime.now()
    print(now.strftime("%H:%M:%S"))
except Exception as e:
    print(f"An error occurred: {str(e)}")
    print("Please check the 'quran_video_creator.log' file for more details.")

input("Press Enter to exit...")