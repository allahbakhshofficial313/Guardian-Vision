import streamlit as st
import pandas as pd

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Guardian Vision",
    page_icon="🛡️",
    layout="wide"
)

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>

.main {
    background-color: #0b1120;
}

.block-container {
    padding-top: 2rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Header */

.header {
    background: linear-gradient(135deg, #111827, #172554);
    padding: 25px 30px;
    border-radius: 18px;
    border: 1px solid #263653;
    margin-bottom: 25px;
}

.header-title {
    font-size: 32px;
    font-weight: 700;
    color: white;
}

.header-subtitle {
    color: #94a3b8;
    font-size: 14px;
    margin-top: 5px;
}

/* Cards */

.card {
    background: #111827;
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #263653;
    min-height: 115px;
}

.card-title {
    color: #94a3b8;
    font-size: 14px;
}

.card-value {
    color: white;
    font-size: 30px;
    font-weight: 700;
    margin-top: 8px;
}

.green {
    color: #22c55e;
}

.red {
    color: #ef4444;
}

.yellow {
    color: #f59e0b;
}

/* Section */

.section-title {
    color: white;
    font-size: 21px;
    font-weight: 600;
    margin-top: 30px;
    margin-bottom: 15px;
}

/* Camera */

.camera-box {
    height: 360px;
    background: #020617;
    border: 2px dashed #334155;
    border-radius: 18px;
    display: flex;
    justify-content: center;
    align-items: center;
    color: #64748b;
    font-size: 20px;
}

/* Detection */

.detection-box {
    background: #111827;
    border: 1px solid #263653;
    border-radius: 16px;
    padding: 20px;
    min-height: 360px;
}

.object-item {
    background: #1e293b;
    padding: 13px;
    border-radius: 10px;
    margin-bottom: 10px;
    color: #e2e8f0;
}

/* Risk */

.risk-box {
    background: #111827;
    border: 1px solid #263653;
    border-radius: 16px;
    padding: 25px;
    text-align: center;
}

.risk-normal {
    color: #22c55e;
    font-size: 28px;
    font-weight: 700;
}

.risk-warning {
    color: #f59e0b;
    font-size: 28px;
    font-weight: 700;
}

.risk-high {
    color: #ef4444;
    font-size: 28px;
    font-weight: 700;
}

/* Footer */

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)


# ==========================================
# HEADER
# ==========================================

st.markdown("""
<div class="header">

<div class="header-title">
🛡️ Guardian Vision AI
</div>

<div class="header-subtitle">
AI-Powered Security Monitoring System
</div>

</div>
""", unsafe_allow_html=True)


# ==========================================
# TOP STATISTICS
# ==========================================

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("""
    <div class="card">
        <div class="card-title">Total Events</div>
        <div class="card-value">528</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card">
        <div class="card-title">High Risk</div>
        <div class="card-value red">94</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card">
        <div class="card-title">Avg Confidence</div>
        <div class="card-value">79.23%</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown("""
    <div class="card">
        <div class="card-title">Objects Detected</div>
        <div class="card-value green">10</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# CAMERA + DETECTIONS
# ==========================================

st.markdown(
    '<div class="section-title">📹 Live Security Monitoring</div>',
    unsafe_allow_html=True
)

camera_col, detection_col = st.columns([2, 1])


# ==========================================
# CAMERA PANEL
# ==========================================

with camera_col:

    st.markdown("""
    <div class="camera-box">
        📷<br>
        Camera Feed
    </div>
    """, unsafe_allow_html=True)

    start_col, stop_col = st.columns(2)

    with start_col:
        st.button(
            "▶️ Start Camera",
            use_container_width=True
        )

    with stop_col:
        st.button(
            "⏹️ Stop Camera",
            use_container_width=True
        )


# ==========================================
# DETECTION PANEL
# ==========================================

with detection_col:

    st.markdown("""
    <div class="detection-box">

    <h3 style="color:white;">
    🔎 Detected Objects
    </h3>

    <div class="object-item">
    👤 Person — 92.4%
    </div>

    <div class="object-item">
    📱 Cell Phone — 87.6%
    </div>

    <div class="object-item">
    🚗 Car — 81.2%
    </div>

    <div class="object-item">
    🥤 Bottle — 76.8%
    </div>

    <div class="object-item">
    💻 Laptop — 72.5%
    </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================
# RISK STATUS
# ==========================================

st.markdown(
    '<div class="section-title">🚨 Security Status</div>',
    unsafe_allow_html=True
)

risk_col1, risk_col2, risk_col3 = st.columns(3)


with risk_col1:

    st.markdown("""
    <div class="risk-box">

    <div style="color:#94a3b8;">
    Camera Status
    </div>

    <div class="risk-normal">
    ● ONLINE
    </div>

    </div>
    """, unsafe_allow_html=True)


with risk_col2:

    st.markdown("""
    <div class="risk-box">

    <div style="color:#94a3b8;">
    Current Risk
    </div>

    <div class="risk-high">
    HIGH RISK
    </div>

    </div>
    """, unsafe_allow_html=True)


with risk_col3:

    st.markdown("""
    <div class="risk-box">

    <div style="color:#94a3b8;">
    AI Model
    </div>

    <div class="risk-normal">
    ● READY
    </div>

    </div>
    """, unsafe_allow_html=True)


# ==========================================
# DETECTION HISTORY
# ==========================================

st.markdown(
    '<div class="section-title">📊 Detection History</div>',
    unsafe_allow_html=True
)


data = {
    "Time": [
        "05:02:55",
        "05:02:45",
        "05:02:35",
        "05:02:25",
        "05:02:15"
    ],
    "Object": [
        "person",
        "cell phone",
        "person",
        "bottle",
        "car"
    ],
    "Confidence": [
        "85.52%",
        "87.60%",
        "92.48%",
        "76.80%",
        "81.20%"
    ],
    "Risk": [
        "WARNING",
        "INFO",
        "HIGH RISK",
        "INFO",
        "NORMAL"
    ]
}

df = pd.DataFrame(data)

st.dataframe(
    df,
    width="stretch",
    hide_index=True
)


# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<div class="footer">
Guardian Vision AI • Intelligent Security Monitoring
</div>
""", unsafe_allow_html=True)