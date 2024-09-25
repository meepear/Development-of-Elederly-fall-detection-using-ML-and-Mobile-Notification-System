import sys
import cv2
import mediapipe as mp
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QFileDialog, QHBoxLayout, QCheckBox, QSpacerItem, QSizePolicy

import math
import time

mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class VideoCaptureThread(QThread):
    frame_received = pyqtSignal(QImage)

    def __init__(self, video_source, show_landmarks=True):
        super().__init__()
        self.cap = cv2.VideoCapture(video_source)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.detection_running = True
        self.show_landmarks = show_landmarks
        self.previous_p_sum = None
        self.paused = False

    def calculate_poin_sum(self, landmarks, w, h):
        x0, y0 = landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x * w, landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y * h
        p_sum = 0

        for landmark in landmarks:
            xi, yi = landmark.x * w, landmark.y * h
            p = math.sqrt((x0 - xi) ** 2 + (y0 - yi) ** 2)
            p_sum += p

        return p_sum

    def run(self):
        while self.detection_running:
            if self.paused:
                time.sleep(0.1)  # หน่วงเวลาเล็กน้อยเมื่อหยุดชั่วคราวเพื่อลดการใช้ CPU
                continue

            ret, frame = self.cap.read()
            if not ret:
                break  # ออกจากลูปเมื่อไม่มีเฟรม

            RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(RGB)

            if results.pose_landmarks:
                landmarks = results.pose_landmarks.landmark
                h, w, c = frame.shape

                current_p_sum = self.calculate_poin_sum(landmarks, w, h)

                if self.previous_p_sum is not None:
                    delta_p = abs(self.previous_p_sum - current_p_sum)

                    # ตรวจจับการล้ม (ความแตกต่างที่มากเกินเกณฑ์)
                    if delta_p > 1000:
                        posture = "Fall Detected"
                        color = (0, 0, 255)
                    else:
                        posture = "Normal"
                        color = (0, 255, 0)

                    # แสดงข้อความการล้ม
                    cv2.putText(frame, posture, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2, cv2.LINE_AA)

                self.previous_p_sum = current_p_sum

                if self.show_landmarks:
                    mp_drawing.draw_landmarks(frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            height, width, channel = frame.shape
            bytes_per_line = 3 * width
            q_image = QImage(frame.data, width, height, bytes_per_line, QImage.Format.Format_BGR888)
            self.frame_received.emit(q_image)

    def set_show_landmarks(self, show_landmarks):
        self.show_landmarks = show_landmarks

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def stop(self):
        self.detection_running = False
        self.wait()
        self.cap.release()

class VideoDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.setFixedSize(640, 480)  # ขนาดเริ่มต้นของ QLabel

        self.load_button = QPushButton("Load Video")
        self.load_button.clicked.connect(self.open_file_dialog)

        self.webcam_button = QPushButton("Switch to Webcam")
        self.webcam_button.clicked.connect(self.switch_to_webcam)

        self.stop_button = QPushButton("Stop Video")
        self.stop_button.clicked.connect(self.stop_video)
        self.stop_button.setEnabled(False)

        self.pause_button = QPushButton("Pause Video")
        self.pause_button.clicked.connect(self.pause_video)
        self.pause_button.setEnabled(False)

        self.resume_button = QPushButton("Resume Video")
        self.resume_button.clicked.connect(self.resume_video)
        self.resume_button.setEnabled(False)

        self.landmark_checkbox = QCheckBox("Show Landmarks")
        self.landmark_checkbox.setChecked(True)
        self.landmark_checkbox.stateChanged.connect(self.toggle_landmarks)

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.webcam_button)
        button_layout.addWidget(self.stop_button)
        button_layout.addWidget(self.pause_button)
        button_layout.addWidget(self.resume_button)
        button_layout.addWidget(self.landmark_checkbox)

        layout = QVBoxLayout()
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.video_thread = None

    def open_file_dialog(self):
        file_dialog = QFileDialog()
        video_path, _ = file_dialog.getOpenFileName(self, "Open Video", "", "Video Files (*.mp4 *.avi *.mov)")
        if video_path:
            self.start_video(video_path)

    def switch_to_webcam(self):
        self.start_video(0)  # 0 is the index for the default webcam

    def start_video(self, video_source):
        if self.video_thread is not None:
            self.stop_video()

        self.video_thread = VideoCaptureThread(video_source, show_landmarks=self.landmark_checkbox.isChecked())
        self.video_thread.frame_received.connect(self.update_image)
        self.video_thread.start()

        self.stop_button.setEnabled(True)
        self.pause_button.setEnabled(True)
        self.resume_button.setEnabled(False)

    def stop_video(self):
        if self.video_thread is not None:
            self.video_thread.stop()
            self.video_thread = None
            self.label.clear()

        self.stop_button.setEnabled(False)
        self.pause_button.setEnabled(False)
        self.resume_button.setEnabled(False)

    def pause_video(self):
        if self.video_thread is not None:
            self.video_thread.pause()
            self.resume_button.setEnabled(True)
            self.pause_button.setEnabled(False)

    def resume_video(self):
        if self.video_thread is not None:
            self.video_thread.resume()
            self.resume_button.setEnabled(False)
            self.pause_button.setEnabled(True)

    def toggle_landmarks(self):
        if self.video_thread is not None:
            self.video_thread.set_show_landmarks(self.landmark_checkbox.isChecked())

    def update_image(self, q_image):
        # ปรับขนาดวิดีโอให้พอดีกับ QLabel โดยรักษาอัตราส่วนภาพ
        pixmap = QPixmap.fromImage(q_image).scaled(self.label.size(), Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
        self.label.setPixmap(pixmap)

    def closeEvent(self, event):
        if self.video_thread is not None:
            self.video_thread.stop()
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = VideoDisplayWidget()
    widget.show()
    sys.exit(app.exec())
