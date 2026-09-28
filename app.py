import streamlit as st
import pandas as pd
import os
import time
import cv2
import av
from datetime import datetime

from ultralytics import YOLO
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase

from risk_engine import check_risk
from event_logger import log_event
from alert_engine import send_alert


# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="Guardian Vision AI",
    page_icon="🛡️",
    layout="wide"
)


# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.header {
    background: linear-gradient(135deg, #111827, #1e3a5f);
    padding: 28px;
    border-radius: 16px;
    color: white;
    margin-bottom: 25px;
}

.header h1 {
    margin: 0;
    font-size: 34px;
}

.header p {
    margin-top: 8px;
    color: #cbd5e1;
}

.metric-card {
    background: white;
    padding: 22px;
    border-radius: 14px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.metric-title {
    color: #64748b;
    font-size: 14px;
}

.metric-value {
    font-size: 30px;
    font-weight: 700;
    color: #111827;
}

.section-title {
    font-size: 23px;
    font-weight: 700;
    margin-top: 25px;
    margin-bottom: 12px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header">
    <h1>🛡️ Guardian Vision AI</h1>
    <p>AI-Powered Security Monitoring System</p>
</div>
""", unsafe_allow_html=True)


# ==========================================
# LOAD YOLO MODEL
# ==========================================

@st.cache_resource
def load_model():
    return YOLO("yolo11n.pt")


model = load_model()


# ==========================================
# CREATE FOLDERS
# ==========================================

os.makedirs("snapshots", exist_ok=True)
os.makedirs("recordings", exist_ok=True)


# ==========================================
# LIVE CAMERA PROCESSOR
# ==========================================

class GuardianVisionProcessor(VideoProcessorBase):

    def __init__(self):

        self.last_alert_time = 0
        self.cooldown = 10

        # Video recording
        self.recording = False
        self.video_writer = None
        self.recording_start_time = 0
        self.recording_duration = 10

    def start_recording(self, frame):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        video_file = os.path.join(
            "recordings",
            f"high_risk_{timestamp}.mp4"
        )

        height, width = frame.shape[:2]

        fourcc = cv2.VideoWriter_fourcc(
            *"mp4v"
        )

        self.video_writer = cv2.VideoWriter(
            video_file,
            fourcc,
            20.0,
            (width, height)
        )

        self.recording = True
        self.recording_start_time = time.time()

        # First frame
        self.video_writer.write(frame)

        print(f"🎥 Recording started: {video_file}")

    def stop_recording(self):

        if self.video_writer is not None:

            self.video_writer.release()
            self.video_writer = None

        self.recording = False

        print("🎥 Recording saved")

    def recv(self, frame):

        img = frame.to_ndarray(format="bgr24")

        current_time = time.time()

        # ==================================
        # RECORDING MODE
        # ==================================

        if self.recording and self.video_writer is not None:

            self.video_writer.write(img)

            elapsed_time = (
                current_time -
                self.recording_start_time
            )

            if elapsed_time >= self.recording_duration:
                self.stop_recording()

            return av.VideoFrame.from_ndarray(
                img,
                format="bgr24"
            )

        # ==================================
        # YOLO DETECTION
        # ==================================

        results = model(
            img,
            verbose=False
        )

        annotated_frame = results[0].plot()

        # ==================================
        # DETECTION & RISK
        # ==================================

        for result in results:

            for box in result.boxes:

                class_id = int(box.cls[0])

                confidence = float(
                    box.conf[0]
                ) * 100

                object_name = model.names[class_id]

                if confidence < 60:
                    continue

                if object_name == "person":

                    risk_level = check_risk(
                        object_name,
                        confidence
                    )

                    if (
                        current_time -
                        self.last_alert_time
                        >= self.cooldown
                    ):

                        log_event(
                            object_name,
                            confidence,
                            risk_level
                        )

                        # ==================================
                        # HIGH RISK → SNAPSHOT
                        # ==================================

                        if risk_level == "HIGH RISK":

                            snapshot_file = time.strftime(
                                "snapshots/high_risk_%Y-%m-%d_%H-%M-%S.jpg"
                            )

                            cv2.imwrite(
                                snapshot_file,
                                annotated_frame
                            )

                        # ==================================
                        # WARNING + HIGH RISK → RECORDING
                        # ==================================

                        if (
                            risk_level in
                            ("WARNING", "HIGH RISK")
                            and not self.recording
                        ):

                            self.start_recording(
                                annotated_frame
                            )

                        # ==================================
                        # MOBILE ALERT
                        # ==================================

                        send_alert(
                            risk_level,
                            object_name,
                            confidence
                        )

                        self.last_alert_time = current_time

                else:

                    log_event(
                        object_name,
                        confidence,
                        "INFO"
                    )

        return av.VideoFrame.from_ndarray(
            annotated_frame,
            format="bgr24"
        )


# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.title("⚙️ Guardian Controls")

st.sidebar.info(
    "Start the camera to begin AI-powered "
    "object detection."
)

st.sidebar.markdown("---")

st.sidebar.write("### System")

st.sidebar.success("🟢 AI Model Ready")

st.sidebar.write(
    "Model: YOLO11n"
)

st.sidebar.write(
    "Detection Threshold: 60%"
)

st.sidebar.write(
    "Alert Cooldown: 10 seconds"
)


# ==========================================
# LIVE CAMERA
# ==========================================

st.markdown(
    '<div class="section-title">📹 Live AI Camera</div>',
    unsafe_allow_html=True
)

webrtc_streamer(
    key="guardian-vision",
    video_processor_factory=GuardianVisionProcessor,
    media_stream_constraints={
        "video": True,
        "audio": False
    },
    async_processing=True
)

# ==========================================
# DETECTION HISTORY
# ==========================================

st.markdown(
    '<div class="section-title">📊 Detection Overview</div>',
    unsafe_allow_html=True
)


if os.path.exists("events.csv"):

    try:

        df = pd.read_csv(
            "events.csv",
            header=None,
            names=[
                "Date",
                "Time",
                "Object",
                "Confidence",
                "Risk"
            ],
            on_bad_lines="skip"
        )

        total_events = len(df)

        high_risk = len(
            df[df["Risk"] == "HIGH RISK"]
        )

        if total_events > 0:
            avg_confidence = df["Confidence"].mean()
        else:
            avg_confidence = 0

        objects = df["Object"].nunique()

        # ======================================
        # METRICS
        # ======================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Total Events</div>
                    <div class="metric-value">{total_events}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">High Risk</div>
                    <div class="metric-value" style="color:#dc2626;">
                        {high_risk}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Avg Confidence</div>
                    <div class="metric-value">
                        {avg_confidence:.2f}%
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with col4:
            st.markdown(
                f"""
                <div class="metric-card">
                    <div class="metric-title">Objects Detected</div>
                    <div class="metric-value" style="color:#16a34a;">
                        {objects}
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        # ======================================
        # TABLE
        # ======================================

        st.markdown(
            '<div class="section-title">📋 Recent Detection History</div>',
            unsafe_allow_html=True
        )

        st.dataframe(
            df.tail(20).iloc[::-1],
            width="stretch",
            hide_index=True
        )

    except Exception as e:

        st.error(
            f"Events file read error: {e}"
        )

else:

    st.info(
        "No detection events recorded yet."
    )


# ==========================================
# SNAPSHOTS
# ==========================================

st.markdown(
    '<div class="section-title">📸 Security Snapshots</div>',
    unsafe_allow_html=True
)

snapshot_files = []

if os.path.exists("snapshots"):

    snapshot_files = [
        f for f in os.listdir("snapshots")
        if f.lower().endswith((".jpg", ".jpeg", ".png"))
    ]


if snapshot_files:

    snapshot_files = sorted(
        snapshot_files,
        reverse=True
    )[:6]

    cols = st.columns(3)

    for i, filename in enumerate(snapshot_files):

        with cols[i % 3]:

            st.image(
                os.path.join(
                    "snapshots",
                    filename
                ),
                caption=filename,
                width="stretch"
            )

else:

    st.info(
        "No security snapshots available."
    )