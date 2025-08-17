from moviepy import VideoFileClip, TextClip, CompositeVideoClip, AudioFileClip, ImageClip, ImageSequenceClip, concatenate_videoclips
import audiofile
from PIL import Image
import streamlit as st
from tempfile import NamedTemporaryFile
import os



st.set_page_config(page_title = 'SM_CODE_IMG_PLUS_AUD', layout = 'wide')
st.header('Image Plus Audio Application')
upload_file_aud = st.file_uploader('Upload the audio file')


if upload_file_aud:
    #audio_bytes = upload_file_aud.read()
    #aud_fnl = st.audio(audio_bytes, format=upload_file_aud.type)
    with NamedTemporaryFile(delete=False) as temp_audio_file: # Add suffix for better compatibility
        temp_audio_file.write(upload_file_aud.getvalue())
        temp_audio_file_path = temp_audio_file.name

    #try:
        # Create an AudioFileClip from the temporary file
       # audio_clip = AudioFileClip(temp_audio_file_path)
        #st.success("Audio file loaded successfully as MoviePy AudioFileClip!")
    #au#dio_bytes = io.BytesIO(upload_file_aud.read())
    af = AudioFileClip(temp_audio_file_path)
    #os.remove(temp_audio_file_path)
    upload_file_img = st.file_uploader('Upload the Image file')
    if upload_file_img:
        top_img = Image.open(upload_file_img, 'r')
        top_img_w, top_img_h = top_img.size
        bottom_img = Image.open('black_background.jpg', 'r')
        bottom_img_w, bottom_img_h = bottom_img.size
        if top_img_w > bottom_img_w or top_img_h >bottom_img_h:
            width_ratio = bottom_img_w / top_img_w
            height_ratio = bottom_img_h / top_img_h
            scale_factor = min(width_ratio, height_ratio)
        else:
            scale_factor = 1


        new_width = int(top_img_w * scale_factor)
        new_height = int(top_img_h * scale_factor)

        resized_img = top_img.resize((new_width, new_height), Image.LANCZOS)

        offset = ((bottom_img_w - new_width) // 2, (bottom_img_h - new_height) // 2)
        bottom_img.paste(resized_img, offset)
        output_name = 'img_fnl.jpg'
        bottom_img.save(output_name)
        my_image_clip = ImageClip(output_name, duration = af.duration)
        my_image_clip.audio = af
        vid = my_image_clip.write_videofile('final_video.mp4',fps =24)
        
        st.success("Video Clip Generated!!")
        video_file = open("final_video.mp4", "rb")
        video_bytes = video_file.read()
        st.video(video_bytes)
