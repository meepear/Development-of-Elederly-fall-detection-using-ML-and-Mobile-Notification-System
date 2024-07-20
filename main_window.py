from PyQt6.QtCore import QSize, Qt
from PyQt6.QtWidgets import (QApplication, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QSizePolicy, QPushButton, QDialog, QCheckBox, QFormLayout)
from PyQt6.QtGui import QPixmap
from video_capture_thread import VideoCaptureThread

class ConfigDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Configuration")
        self.setFixedSize(QSize(300, 200))
        layout = QFormLayout()
        self.setLayout(layout)
        for option in ["Option 1", "Option 2", "Option 3"]:
            layout.addRow(QCheckBox(option))

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fall Down Detection")
        self.setFixedSize(QSize(1600, 900))

        # Main layout with 3 columns
        main_layout = QHBoxLayout(self)

        # Left column with buttons centered
        left_column = QVBoxLayout()
        left_column.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for text, handler in [("Config", self.open_config_dialog), ("Exit", self.close)]:
            button = QPushButton(text)
            button.setFixedSize(QSize(150, 100))
            button.clicked.connect(handler)
            left_column.addWidget(button)
        main_layout.addLayout(left_column)

        # Center column for video
        self.image_label = QLabel()
        self.image_label.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        main_layout.addWidget(self.image_label)

        # Right column for notifications
        right_column = QVBoxLayout()
        right_column.addWidget(QLabel("Notifications go here"))
        main_layout.addLayout(right_column)

        # Start video thread
        self.video_thread = VideoCaptureThread()
        self.video_thread.frame_received.connect(self.update_image)
        self.video_thread.start()

    def open_config_dialog(self):
        ConfigDialog(self).exec()

    def update_image(self, q_image):
        pixmap = QPixmap.fromImage(q_image)
        pixmap = pixmap.scaled(self.image_label.size(), Qt.AspectRatioMode.KeepAspectRatio)
        self.image_label.setPixmap(pixmap)

    def closeEvent(self, event):
        self.video_thread.stop()
        event.accept()

# Run the application
if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
