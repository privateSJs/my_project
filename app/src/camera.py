import cv2
from ultralytics import YOLO
from app.config.config import MODEL_TRAINED_FILE

cap = cv2.VideoCapture(0)  # Jeśli nie działa, spróbuj zmienić na 1 lub 2

while True:
    ret, frame = cap.read()
    if not ret:
        print("Nie udało się przechwycić obrazu")
        break

    cv2.imshow("Test kamery w OpenCV", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
