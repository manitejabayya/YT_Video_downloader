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


link = st.text_input("Enter the video link below:", "")
email = st.text_input("Enter your Email ID:")
password = st.text_input("Enter your Password:", type="password")


download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)


logging.basicConfig(level=logging.INFO)

def get_cookies(email, password):
    
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  
    driver = webdriver.Chrome(options=options)

    try:
        
        driver.get("https://accounts.google.com/ServiceLogin?service=youtube")

       
        email_elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "identifierId"))
        )
        email_elem.send_keys(email)
        email_elem.send_keys(Keys.RETURN)

       
        password_elem = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)

        
        time.sleep(5)  

        
        WebDriverWait(driver, 30).until(
            EC.url_changes("https://accounts.google.com/ServiceLogin?service=youtube")
        )

        
        if driver.current_url == "https://accounts.google.com/signin/v2/identifier":
            logging.error("Login failed. Please check your credentials.")
            st.error("Login failed. Please check your credentials.")
            driver.quit()
            return None

        
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

if st.button("Login & Generate Cookies"):
    if email and password:
        st.info("Logging in and generating cookies, please wait...")
        get_cookies(email, password)
    else:
        st.warning("⚠️ Please enter valid email and password.")

cookies_file = st.file_uploader("Upload your cookies.txt file for YouTube login", type="txt")

if st.button("Download"):
    if link:
        if cookies_file:
            
            with open("cookies.txt", "wb") as f:
                f.write(cookies_file.getbuffer())
            
            st.info("Downloading, please wait...")

           
            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',  
                'outtmpl': os.path.join(download_dir, 'Downloaded_Video.%(ext)s'),  
                'cookiefile': 'cookies.txt', 
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                
                downloaded_file = [f for f in os.listdir(download_dir) if f.startswith("Downloaded_Video")][0]
                video_path = os.path.join(download_dir, downloaded_file)

                
                with open(video_path, 'rb') as file:
                    st.download_button(
                        label="Click to Download the Video",
                        data=file,
                        file_name=downloaded_file,
                        mime="video/mp4"  
                    )
                st.success("✅ Download completed! Click the button to download your video.")
            except Exception as e:
                logging.error(f"❌ Failed to download the video. Error: {str(e)}")
                st.error(f"❌ Failed to download the video. Error: {str(e)}")
        else:
            st.warning("⚠️ Please upload your cookies.txt file to authenticate.")
    else:
        st.warning("⚠️ Please enter a valid video link.")


st.markdown("""
    ---
    Developed by **Bayya Maniteja**  
    Powered by [yt-dlp](https://github.com/yt-dlp/yt-dlp)
""")
