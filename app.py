import streamlit as st
import yt_dlp
import os

# Set page title and layout to make it look modern
st.set_page_config(page_title="Pro YouTube Downloader", page_icon="🎥", layout="centered")

# --- CUSTOM INTERFACE STYLING (FANCY BLUE/DARK ACCENTS) ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stButton>button {
        width: 100%;
        background-color: #ff0000;
        color: white;
        font-weight: bold;
        border-radius: 8px;
        border: none;
        padding: 10px;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #cc0000;
        color: white;
    }
    .instruction-box {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# App Heading
st.title("🎥 Ultimate YouTube Video Downloader")
st.caption("Paste a YouTube link below, fetch the file, and save it directly to your local storage.")

# --- HOW TO DOWNLOAD INSTRUCTIONS (FANCY BOX) ---
st.markdown("""
<div class="instruction-box">
    <h3>📖 How to Use and Save Videos to Your Device</h3>
    <p>Follow these quick steps to transfer any video straight to your phone or computer storage:</p>
    <ol>
        <li><b>Copy the Link:</b> Go to YouTube, open your desired video, and copy the full URL from your browser address bar (or tap 'Share' and copy the link on mobile).</li>
        <li><b>Fetch the Video:</b> Paste the link into the input field below and hit the red <b>"Process Video"</b> button.</li>
        <li><b>Server Generation:</b> Wait a few moments. Our cloud script will connect to YouTube, extract the video framework, and prepare the clean file container.</li>
        <li><b>Save locally:</b> Once processing finishes, a green <b>"Download to Your Device"</b> button will pop up. Click it to choose exactly where to save the MP4 file on your local phone or PC storage!</li>
    </ol>
</div>
""", unsafe_allow_html=True)

# --- WORKSPACE INTERFACE ---
st.subheader("🔗 Paste Your Video Link Here")
video_url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...")

if st.button("Process Video"):
    if not video_url:
        st.error("Please paste a valid YouTube URL first!")
    else:
        with st.spinner("Connecting to YouTube and processing the file... Please wait."):
            try:
                # Configuration layout for yt-dlp to grab standard combined MP4 formats
                ydl_opts = {
                    'format': 'best[ext=mp4]/best',
                    'outtmpl': 'downloaded_video.mp4',
                    'noplaylist': True,
                }
                
                # Remove old file if it exists to clean space
                if os.path.exists("downloaded_video.mp4"):
                    os.remove("downloaded_video.mp4")
                
                # Execute extraction
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info_dict = ydl.extract_info(video_url, download=True)
                    video_title = info_dict.get('title', 'video')
                
                st.success(f"Successfully processed: **{video_title}**")
                
                # Read the file back as binary data to give to the user's browser download utility
                with open("downloaded_video.mp4", "rb") as file:
                    st.download_button(
                        label="📥 Download to Your Device",
                        data=file,
                        file_name=f"{video_title}.mp4",
                        mime="video/mp4"
                    )
                    
            except Exception as e:
                st.error(f"An error occurred during extraction: {str(e)}")