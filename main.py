import cv2

from app.face_detector import FaceDetector
from app.sticker_applier import StickerApplier

# Initialize the webcam
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

face_detector = FaceDetector("data/deploy.prototxt", "data/face_detector.caffemodel")
sticker_applier = StickerApplier('data/laughing_man.png')

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break

        faces = face_detector.detect_faces(frame)
        sticker_applier.apply_sticker(frame, faces)

        cv2.imshow('Laughing man', frame)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
except KeyboardInterrupt:
    # Handle manual interruption (Ctrl+C, etc.)
    pass
finally:
    # Ensure resources are released properly
    cap.release()
    # out.release()
    cv2.destroyAllWindows()