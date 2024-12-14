import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import yt_dlp
import pickle
import logging

st.title("🎥 Video Downloader with yt-dlp (Login-based)")

# Input for the video link and user credentials
link = st.text_input("Enter the video link below:", "")
email = st.text_input("Enter your Email ID:")
password = st.text_input("Enter your Password:", type="password")

# Directory to save the downloaded video
download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)

# Setup logging
logging.basicConfig(level=logging.INFO)

# Function to login to YouTube and extract cookies
def get_cookies(email, password):
    # Setup Selenium WebDriver with Chrome
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (without opening the browser window)
    driver = webdriver.Chrome(options=options)

    try:
        # Open YouTube login page
        driver.get("https://accounts.google.com/ServiceLogin?service=youtube")

        # Wait for the email input field to load and send email
        email_elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_elem.send_keys(email)
        email_elem.send_keys(Keys.RETURN)

        # Wait for the password field and send password
        password_elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)

        # Wait for login completion (may take time)
        time.sleep(5)  # Give extra time to load after login

        # Handle potential CAPTCHA or verification page
        WebDriverWait(driver, 30).until(
            EC.url_changes("https://accounts.google.com/ServiceLogin?service=youtube")
        )

        # Check if login was successful
        if driver.current_url == "https://accounts.google.com/signin/v2/identifier":
            logging.error("Login failed. Please check your credentials.")
            st.error("Login failed. Please check your credentials.")
            driver.quit()
            return None

        # Get cookies and save them to a file
        cookies = driver.get_cookies()
        with open("cookies.txt", "w") as cookie_file:
            for cookie in cookies:
                cookie_file.write(f"{cookie['name']}={cookie['value']};\n")

        logging.info("Cookies saved successfully.")
        st.success("Cookies generated successfully!")

    except Exception as e:
        logging.error(f"Error during login: {e}")
        st.error(f"Error during login: {e}")
    finally:
        driver.quit()

# Ask the user to login and generate cookies if credentials are provided
if st.button("Login & Generate Cookies"):
    if email and password:
        st.info("Logging in and generating cookies, please wait...")
        get_cookies(email, password)
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
                logging.error(f"❌ Failed to download the video. Error: {str(e)}")
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
