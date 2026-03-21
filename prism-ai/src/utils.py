import cv2
import numpy as np
from PIL import Image
import datetime


def PIL_to_opencv(pil_image):
    """Convert a PIL image (used by Streamlit) to OpenCV format (BGR)."""
    # Convert RGB to BGR
    return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)


def opencv_to_PIL(cv2_image):
    """Convert an OpenCV image (BGR) back to PIL format for Streamlit display."""
    # Convert BGR to RGB
    return Image.fromarray(cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB))


def get_detection_summary(results):
    """
    Parses YOLO results to create a dictionary of detected objects and their counts.
    Example: {'person': 2, 'dog': 1}
    """
    summary = {}
    if results[0].boxes:
        for box in results[0].boxes:
            # Get class name from the model's names dictionary
            cls_id = int(box.cls[0])
            label = results[0].names[cls_id]
            summary[label] = summary.get(label, 0) + 1
    return summary


def generate_report_text(summary):
    """Creates a professional text summary for the detection report."""
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report = f"Prism AI - Detection Report\n"
    report += f"Generated on: {timestamp}\n"
    report += "-" * 30 + "\n"

    if not summary:
        report += "No objects detected in the scene.\n"
    else:
        for obj, count in summary.items():
            report += f"- {obj.capitalize()}: {count}\n"

    report += "-" * 30 + "\n"
    return report


def resize_image(image, width=800):
    """Resizes an image while maintaining aspect ratio for better UI performance."""
    h, w = image.shape[:2]
    aspect_ratio = h / w
    new_height = int(width * aspect_ratio)
    return cv2.resize(image, (width, new_height))