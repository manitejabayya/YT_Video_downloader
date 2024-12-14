import os
import time
import streamlit as st
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import yt_dlp

st.title("🎥 Video Downloader with yt-dlp (Login-based)")

# Input fields for user credentials and video link
link = st.text_input("Enter the video link below:", "")
email = st.text_input("Enter your Email ID:")
password = st.text_input("Enter your Password:", type="password")

# Directory to save the downloaded video
download_dir = './downloads'
os.makedirs(download_dir, exist_ok=True)

# Function to login to YouTube and extract cookies
def get_cookies(email, password, headless=True):
    # Setup Selenium WebDriver
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    driver = webdriver.Chrome(options=options)
    wait = WebDriverWait(driver, 30)  # Wait up to 30 seconds for elements
    
    try:
        # Open Google login page
        driver.get("https://accounts.google.com/ServiceLogin?service=youtube")
        st.info("Opened Google login page.")
        
        # Enter email
        email_elem = wait.until(EC.visibility_of_element_located((By.ID, "identifierId")))
        driver.execute_script("arguments[0].scrollIntoView();", email_elem)  # Scroll to make element visible
        email_elem.click()  # Ensure the element is interactable
        email_elem.send_keys(email)
        email_elem.send_keys(Keys.RETURN)
        st.info("Entered email.")
        
        # Wait for password input
        password_elem = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))
        )
        driver.execute_script("arguments[0].scrollIntoView();", password_elem)  # Scroll to make element visible
        password_elem.send_keys(password)
        password_elem.send_keys(Keys.RETURN)
        st.info("Entered password.")
        
        # Wait for successful login (use a check for the next page)
        wait.until(EC.url_contains("myaccount.google.com"))
        st.success("Login successful!")

        # Save cookies to file
        cookies = driver.get_cookies()
        with open("cookies.txt", "w") as cookie_file:
            for cookie in cookies:
                cookie_file.write(f"{cookie['name']}={cookie['value']};\n")
        
        st.success("Cookies generated successfully!")
    except TimeoutException as e:
        driver.save_screenshot("timeout_error.png")
        st.error("❌ Timeout error. Screenshot saved as 'timeout_error.png'.")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    except NoSuchElementException as e:
        driver.save_screenshot("nosuchelement_error.png")
        st.error("❌ Element not found. Screenshot saved as 'nosuchelement_error.png'.")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    except Exception as e:
        driver.save_screenshot("unexpected_error.png")
        st.error(f"❌ An unexpected error occurred: {str(e)}. Screenshot saved as 'unexpected_error.png'.")
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
    finally:
        driver.quit()



# Login and generate cookies
if st.button("Login & Generate Cookies"):
    if email and password:
        st.info("Logging in and generating cookies, please wait...")
        get_cookies(email, password, headless=False)  # Set headless=False for debugging
    else:
        st.warning("⚠️ Please enter valid email and password.")

# Upload cookies for authentication
cookies_file = st.file_uploader("Upload your cookies.txt file for YouTube login", type="txt")

# Download video
if st.button("Download"):
    if link:
        if cookies_file:
            with open("cookies.txt", "wb") as f:
                f.write(cookies_file.getbuffer())
            
            st.info("Downloading video, please wait...")

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
                'outtmpl': os.path.join(download_dir, 'Downloaded_Video.%(ext)s'),
                'cookiefile': 'cookies.txt',
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])

                # Dynamically get downloaded file
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
