import streamlit as st
import yt_dlp


st.title("🎥 Video Downloader with yt-dlp")
st.write("Download videos from YouTube and other platforms easily!")

# Input for the video link
link = st.text_input("Enter the video link below:", "")


if st.button("Download"):
    if link:
        st.info("Downloading, please wait...")
        
       
        ydl_opts = {
            'format': 'best',  
            'outtmpl': 'Downloaded_Video.%(ext)s',  
        }

       
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])
            st.success("✅ Download completed! Check your file named 'Downloaded_Video'.")
        except Exception as e:
            st.error(f"❌ Failed to download the video. Error: {str(e)}")
    else:
        st.warning("⚠️ Please enter a valid video link.")


st.markdown("""
    ---
    Developed by **Bayya Maniteja**  
    Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
""")
