import streamlit as st
import cv2
import numpy as np
from PIL import Image
from src.detector import ObjectDetector

# --- Times New Roman Styling ---
st.markdown(
    """
    <style>
    * { font-family: "Times New Roman", Times, serif !important; }
    .main-title { font-size: 40px; font-weight: bold; text-align: center; color: #1E3A8A; }
    .stat-box { padding: 10px; border-radius: 5px; background-color: #F3F4F6; text-align: center; font-size: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown('<div class="main-title">Prism AI: Object Detection System</div>', unsafe_allow_html=True)

# Initialize detector
detector = ObjectDetector()

# Sidebar options
option = st.sidebar.selectbox("Choose Input Source", ("Upload Image", "Live Webcam"))

if option == "Upload Image":
    # Change st.file_upload to st.file_uploader
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Convert file to OpenCV format
        image = Image.open(uploaded_file)
        img_array = np.array(image)

        # Process detection
        with st.spinner('Analyzing pixels...'):
	    # Add this before calling detect
	    img_array = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
            processed_img, count = detector.detect(img_array)

        # Display Results
        st.image(processed_img, caption=f"Detection Results", use_column_width=True)
        st.markdown(f'<div class="stat-box">Objects Detected: {count}</div>', unsafe_allow_html=True)

elif option == "Live Webcam":
    st.warning("Note: Webcam features work best on local host.")
    run = st.checkbox('Start Webcam')
    FRAME_WINDOW = st.image([])
    camera = cv2.VideoCapture(0)

    while run:
        ret, frame = camera.read()
        if not ret:
            st.error("Failed to access webcam.")
            break

        # Convert BGR to RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect
        processed_frame, count = detector.detect(frame)

        # Update UI
        FRAME_WINDOW.image(processed_frame)
    else:
        camera.release()
        st.write("Webcam stopped.")
