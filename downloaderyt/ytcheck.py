import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import yt_dlp
import pickle

st.title("🎥 Video Downloader with yt-dlp (Login-based)")

# Input for the video link and user credentials
link = st.text_input("Enter the video link below:", "")
email = st.text_input("Enter your Email ID:")
password = st.text_input("Enter your Password:", type="password")

# Directory to save the downloaded video
download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)

# Function to login to YouTube and extract cookies
def get_cookies(email, password):
    # Setup Selenium WebDriver with Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (without opening the browser window)
    driver = webdriver.Chrome(options=options)

    # Open YouTube login page
    driver.get("https://accounts.google.com/ServiceLogin?service=youtube")

    # Find and fill the email and password fields
    email_elem = driver.find_element(By.ID, "identifierId")
    email_elem.send_keys(email)
    email_elem.send_keys(Keys.RETURN)
    time.sleep(2)

    password_elem = driver.find_element(By.NAME, "password")
    password_elem.send_keys(password)
    password_elem.send_keys(Keys.RETURN)
    time.sleep(5)  # Wait for login to complete

    # Wait for cookies to be generated and saved by the browser
    cookies = driver.get_cookies()

    # Save cookies in a file (cookies.txt format)
    with open("cookies.txt", "w") as cookie_file:
        for cookie in cookies:
            cookie_file.write(f"{cookie['name']}={cookie['value']};\n")
    
    driver.quit()

# Ask the user to login and generate cookies if credentials are provided
if st.button("Login & Generate Cookies"):
    if email and password:
        st.info("Logging in and generating cookies, please wait...")
        get_cookies(email, password)
        st.success("Cookies generated successfully!")
    else:
        st.warning("⚠️ Please enter valid email and password.")

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
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  # Prefer mp4 video and m4a audio
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
                        mime="video/mp4"  # Use appropriate mime type for mp4
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
