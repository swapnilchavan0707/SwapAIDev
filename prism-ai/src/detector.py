from ultralytics import YOLO
import cv2


class ObjectDetector:
    def __init__(self, model_path='yolov8n.pt'):
        # Load the pre-trained YOLOv8 Nano model (small and fast)
        self.model = YOLO(model_path)

    def detect(self, image):
        # Run inference
        results = self.model(image)

        # Plot results on the image (draws boxes and labels)
        annotated_image = results[0].plot()

        # Get count of objects detected
        count = len(results[0].boxes)

        return annotated_image, count
