import os
import streamlit as st
import yt_dlp

st.title("🎥 Video Downloader with yt-dlp")
st.write("Download videos from YouTube and other platforms easily!")

# Input for the video link
link = st.text_input("Enter the video link below:", "")

# Temporary directory to save the video
download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)

if st.button("Download"):
    if link:
        st.info("Downloading, please wait...")
        
        ydl_opts = {
            'format': 'best',  
            'outtmpl': os.path.join(download_dir, 'Downloaded_Video.%(ext)s'),  
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])

            video_path = os.path.join(download_dir, 'Downloaded_Video.mp4')  # Adjust extension if needed

            # Display a download button to download the video file
            with open(video_path, 'rb') as file:
                st.download_button(
                    label="Click to Download the Video",
                    data=file,
                    file_name='Downloaded_Video.mp4',
                    mime="video/mp4"
                )
            st.success("✅ Download completed! Click the button to download your video.")
        except Exception as e:
            st.error(f"❌ Failed to download the video. Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid video link.")

st.markdown("""
    ---
    Developed by **Bayya Maniteja**  
    Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
""")
