import streamlit as st
import os
import tempfile
from concurrent.futures import ThreadPoolExecutor
import subprocess

# Function for adding watermark using FFmpeg system command
def add_watermark(video_path, watermark_path, output_path, position):
    command = ['ffmpeg', '-y', '-i', video_path, '-i', watermark_path, '-filter_complex', f"overlay={position}", '-codec:a', 'copy', output_path]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def main():
    st.title("Watermark Adder")

    # File uploader for watermark image
    watermark = st.file_uploader("Upload a Watermark", type=['png'])

    # File uploader for videos
    videos = st.file_uploader("Upload Videos", type=['mp4', 'mkv', 'flv', 'avi'], accept_multiple_files=True)

    # Position of the watermark
    position_options = {
        'Bottom-right': 'main_w-overlay_w-10:main_h-overlay_h-10',
        'Bottom-left': '10:main_h-overlay_h-10',
        'Top-left': '10:10',
        'Top-right': 'main_w-overlay_w-10:10',
    }
    position = st.selectbox('Watermark Position', list(position_options.keys()))

    if watermark is None or videos is None:
        st.error('Please upload both a watermark and at least one video before starting watermarking.')

    elif st.button('Start watermarking'):
        with st.spinner('Watermarking in progress...'):
            with ThreadPoolExecutor(max_workers=4) as executor:
                for video in videos:
                    # Create temporary files for I/O
                    with tempfile.NamedTemporaryFile(delete=False, suffix='.png') as watermark_file, \
                            tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as video_file, \
                            tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as output_file:

                        # Write the uploaded image and video to the temporary files
                        watermark_file.write(watermark.getvalue())
                        watermark_file.flush()

                        video_file.write(video.getvalue())
                        video_file.flush()

                        # Add watermark to the video
                        executor.submit(add_watermark, video_file.name, watermark_file.name, output_file.name,
                                        position_options[position])

                        # Display a link to download the output video
                        with open(output_file.name, "rb") as file:
                            bytes = file.read()
                            st.download_button(
                                label="Download watermarked video",
                                data=bytes,
                                file_name="watermarked_video.mp4",
                                mime="video/mp4",
                            )

        st.success('Watermarking completed.')

if __name__ == "__main__":
    main()
