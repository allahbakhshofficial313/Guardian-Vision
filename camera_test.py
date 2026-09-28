import streamlit as st
import cv2
from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
import av


st.set_page_config(
    page_title="Guardian Vision AI",
    page_icon="🛡️",
    layout="wide"
)


# ==============================
# PAGE
# ==============================

st.title("🛡️ Guardian Vision AI")
st.caption("Live AI Security Monitoring System")


# ==============================
# LOAD YOLO
# ==============================

@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")


model = load_model()


# ==============================
# CAMERA PROCESSOR
# ==============================

class GuardianVision(VideoTransformerBase):

    def transform(self, frame):

        img = frame.to_ndarray(format="bgr24")

        results = model(
            img,
            verbose=False,
            conf=0.50
        )

        annotated = results[0].plot()

        return annotated


# ==============================
# STATUS
# ==============================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Camera", "LIVE")

with col2:
    st.metric("AI Model", "YOLO11n")

with col3:
    st.metric("Status", "Monitoring")


st.divider()


# ==============================
# LIVE CAMERA
# ==============================

st.subheader("📹 Live Security Camera")

webrtc_streamer(
    key="guardian-camera",
    video_transformer_factory=GuardianVision,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)


st.divider()

st.info(
    "Guardian Vision is monitoring the camera feed using YOLO object detection."
)