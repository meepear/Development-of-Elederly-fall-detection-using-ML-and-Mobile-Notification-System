import sys
import cv2

import mediapipe as mp

from PyQt6.QtCore import QObject, Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QCheckBox, QSpacerItem, QSizePolicy


mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

class VideoCaptureThread(QThread):
    frame_received = pyqtSignal(QImage)
    def __init__(self, show_pointer):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        self.detection_running = True

    def run(self):
        while self.detection_running:
            if self.detection_running:
                continue

            ret, frame = self.cap.read()
            if not ret:
                continue

            RGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = self.pose.process(RGB)

            


class VideoDisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.label = QLabel()
        self.label.setFixedSize(640, 480)

        self.start_button = QPushButton("Start")        
        self.stop_button = QPushButton("Stop")
        self.stop_button.setEnabled(False)

        # Layouts
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.start_button)
        button_layout.addWidget(self.stop_button)

        layout = QVBoxLayout()
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addWidget(self.label, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addItem(QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding))
        layout.addLayout(button_layout)
        self.setLayout(layout)

        self.video_thread = None

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = VideoDisplayWidget()
    widget.show()
    sys.exit(app.exec())