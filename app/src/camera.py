import cv2
from ultralytics import YOLO
from app.config.config import MODEL_TRAINED_FILE

for i in range(5):  # Testujemy kilka indeksów
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"✅ Kamera dostępna na indeksie {i}")
        cap.release()
    else:
        print(f"❌ Kamera niedostępna na indeksie {i}")
