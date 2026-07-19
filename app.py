import streamlit as st
import yt_dlp
import os

# Set page layout
st.set_page_config(page_title="Speed Downloader Pro", page_icon="⚡", layout="centered")

# --- HIGH-CONTRAST GOLD & DARK GLOW STYLING ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f14 !important;
    }
    h1, h2, h3, p, span, label {
        color: #f0f6fc !important;
    }
    .stTextInput input {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 2px solid #30363d !important;
        border-radius: 8px !important;
    }
    
    /* Re-colored Instruction Paragraph Box */
    .instruction-box {
        background-color: #161b22;
        padding: 24px;
        border-radius: 12px;
        border: 2px solid #ffc107;
        box-shadow: 0px 0px 20px rgba(255, 193, 7, 0.15);
        margin-bottom: 25px;
    }
    .instruction-box h3 {
        color: #ffc107 !important;
        margin-top: 0;
        font-weight: bold;
    }
    .instruction-box ol li {
        color: #ffe082 !important;
        margin-bottom: 10px;
        line-height: 1.6;
        font-size: 16px;
    }
    .instruction-box b {
        color: #ffffff !important;
        text-decoration: underline;
    }

    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #1f6feb, #58a6ff) !important;
        color: white !important;
        font-weight: bold !important;
        border-radius: 8px !important;
        border: none !important;
        padding: 12px !important;
        box-shadow: 0 4px 12px rgba(31, 111, 235, 0.3);
    }
    .stButton>button:hover {
        background: linear-gradient(90deg, #58a6ff, #1f6feb) !important;
        box-shadow: 0 6px 16px rgba(31, 111, 235, 0.5);
    }
    </style>
""", unsafe_allow_html=True)

st.title("⚡ Speed Downloader Pro")
st.caption("High-velocity direct YouTube local media extractor.")

st.markdown("""
<div class="instruction-box">
    <h3>📖 Instruction Guide: How to Store Videos on Your Device</h3>
    <ol>
        <li><b>Copy Link:</b> Open YouTube on your phone or PC, select your favorite video, and copy the full URL string from your address bar.</li>
        <li><b>Inject Link:</b> Paste that clean address directly into the field box down below.</li>
        <li><b>Stream File:</b> Hit the blue <b>"Process Video"</b> button. The cloud framework will instantly establish an open channel connection.</li>
        <li><b>Commit Storage:</b> Once the green download button surfaces, press it to assign a local file folder destination path on your hardware device!</li>
    </ol>
</div>
""", unsafe_allow_html=True)

st.subheader("🔗 Paste Your Video Link")
video_url = st.text_input("YouTube URL:", placeholder="https://www.youtube.com/watch?v=...", label_visibility="collapsed")

if st.button("Process Video"):
    if not video_url:
        st.error("Please insert a link first!")
    else:
        status_box = st.empty()
        status_box.info("⚡ Synchronizing browser emulation layers... Please wait.")
        
        try:
            # ENHANCED FIX TO OVERRIDE THE 403 FORBIDDEN BLOCKS
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': 'speed_cache.mp4',
                'noplaylist': True,
                'quiet': True,
                'rm_cachedir': True,
                'impersonate': 'chrome', # Spoofs request header as a full desktop Chrome browser
                'extractor_args': {
                    'youtube': {
                        'player_client': ['web', 'default'],
                        'player_skip': ['web_embedded', 'ios_downgraded'] # Drops restricted endpoints
                    }
                }
            }
            
            if os.path.exists("speed_cache.mp4"):
                os.remove("speed_cache.mp4")
                
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                title = info.get('title', 'Downloaded_Video')
            
            status_box.empty()
            st.success(f"🎉 Ready! Extraction Completed: **{title}**")
            
            with open("speed_cache.mp4", "rb") as f:
                video_bytes = f.read()
                
            st.download_button(
                label="📥 Click to Save Directly to Device Storage",
                data=video_bytes,
                file_name=f"{title}.mp4",
                mime="video/mp4"
            )
            
        except Exception as e:
            status_box.empty()
            st.error(f"Execution boundary crossed: {str(e)}")