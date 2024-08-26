import sys
import cv2
import mediapipe as mp
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

# Initializing MediaPipe Pose and Drawing utilities
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class VideoCaptureThread(QThread):
    frame_received = pyqtSignal(QImage)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture('res/TestVDO.mp4')
        self.pose = mp_pose.Ppose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.detection_running = True

    def run(self):
        while self.detection_running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(RGB)

            if results.pose_landmarks:
                # Draw pose landmarks and connections
                mp_drawing.draw_landmarks(
                    frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                    mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=2, circle_radius=2),
                    mp_drawing.DrawingSpec(color=(0, 0, 255), thickness=2, circle_radius=2)
                )

                landmarks = results.pose_landmarks.landmark
                h, w, c = frame.shape
                x_min, x_max = w, 0
                y_min, y_max = h, 0

                for idx, landmark in enumerate(landmarks):
                    cx, cy = int(landmark.x * w), int(landmark.y * h)
                    cv2.circle(frame, (cx, cy), 5, (0, 0, 255), -1)
                    cv2.putText(frame, f'{idx}', (cx - 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2, cv2.LINE_AA)
                    cv2.putText(frame, f'({cx}, {cy})', (cx + 10, cy + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.3, (255, 255, 255), 1, cv2.LINE_AA)
                    x_min = min(x_min, cx)
                    x_max = max(x_max, cx)
                    y_min = min(y_min, cy)
                    y_max = max(y_max, cy)

                cv2.rectangle(frame, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)

                left_hip = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value]
                right_hip = landmarks[mp_pose.PoseLandmark.RIGHT_HIP.value]
                left_ankle = landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value]
                right_ankle = landmarks[mp_pose.PoseLandmark.RIGHT_ANKLE.value]

                if (left_hip.y < left_ankle.y) and (right_hip.y < right_ankle.y):
                    posture = "Stand"
                    color = (0, 255, 0)
                else:
                    posture = "Fell Down"
                    color = (0, 0, 255)

                cx, cy = int((left_hip.x + right_hip.x) / 2 * w), int((left_hip.y + right_hip.y) / 2 * h)
                cv2.putText(frame, posture, (cx, cy - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            self.frame_received.emit(q_image)

    def stop(self):
        self.detection_running = False
        self.wait()
        self.cap.release()

class VideoDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.setFixedSize(640, 480)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.video_thread = VideoCaptureThread()
        self.video_thread.frame_received.connect(self.update_image)
        self.video_thread.start()

    def update_image(self, q_image):
        self.label.setPixmap(QPixmap.fromImage(q_image))

    def closeEvent(self, event):
        self.video_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = VideoDisplayWidget()
    widget.show()
    sys.exit(app.exec())
