import os
import streamlit as st
import yt_dlp

st.title("🎥 Video Downloader with yt-dlp")
st.write("Download videos from YouTube and other platforms easily!")

# Input for the video link
link = st.text_input("Enter the video link below:", "")

# Directory to save the downloaded video
download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)

# Ask the user to upload the cookies.txt file for authentication
cookies_file = st.file_uploader("Upload your cookies.txt file for YouTube login", type="txt")

if st.button("Download"):
    if link:
        if cookies_file:
            # Save the uploaded cookies file temporarily
            with open("cookies.txt", "wb") as f:
                f.write(cookies_file.getbuffer())
            
            st.info("Downloading, please wait...")

            # Set download options with the cookies.txt file for YouTube authentication
            ydl_opts = {
                'format': 'best',  # Best available format
                'outtmpl': os.path.join(download_dir, 'Downloaded_Video.%(ext)s'),  # Output file template
                'cookiefile': 'cookies.txt',  # Path to the cookies.txt file
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                # Get the downloaded file path dynamically (handles different formats)
                downloaded_file = [f for f in os.listdir(download_dir) if f.startswith("Downloaded_Video")][0]
                video_path = os.path.join(download_dir, downloaded_file)

                # Provide a download button for the user to download the video
                with open(video_path, 'rb') as file:
                    st.download_button(
                        label="Click to Download the Video",
                        data=file,
                        file_name=downloaded_file,
                        mime="video/mp4"  # Use appropriate mime type if needed (e.g., video/webm)
                    )
                st.success("✅ Download completed! Click the button to download your video.")
            except Exception as e:
                st.error(f"❌ Failed to download the video. Error: {str(e)}")
        else:
            st.warning("⚠️ Please upload your cookies.txt file to authenticate.")
    else:
        st.warning("⚠️ Please enter a valid video link.")

# Footer with credits
st.markdown("""
    ---
    Developed by **Bayya Maniteja**  
    Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
""")
