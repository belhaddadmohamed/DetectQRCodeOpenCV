import cv2
from pyzbar.pyzbar import decode
import numpy as np

def main():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot access camera")
        return

    print("Press 'q' to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        decoded_objects = decode(frame)

        for obj in decoded_objects:
            # Get points as a numpy array
            points = obj.polygon
            pts = np.array([(p.x, p.y) for p in points], dtype=np.int32)

            # Draw polygon around QR code
            cv2.polylines(frame, [pts], isClosed=True, color=(0, 255, 0), thickness=2)

            # Display QR data
            qr_data = obj.data.decode("utf-8")
            qr_type = obj.type
            cv2.putText(frame, f"{qr_data} ({qr_type})",
                        (pts[0][0], pts[0][1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

            print(f"Detected: {qr_data} - Type: {qr_type}")

        cv2.imshow("QR Code Scanner", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
