import sys
import cv2
import time
import os
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout, QFileDialog, QMessageBox

class VideoCaptureThread(QThread):
    frame_received = pyqtSignal(QImage)
    time_updated = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.running = True
        self.is_recording = False
        self.out = None
        self.start_time = None
        
        # HIGHT_VALUE = 10000
        WIDTH = 1280
        HEIGHT = 720
        FPS = 30
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)

    def start_recording(self, save_path):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(save_path, fourcc, self.fps, (self.width, self.height)) 
        self.start_time = time.time()  # เก็บเวลาที่เริ่มต้น
        self.is_recording = True

    def stop_recording(self):
        if self.out is not None:
            self.out.release() 
        self.is_recording = False
        self.start_time = None

    def stop(self):
        self.running = False

    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue

            # บันทึกวิดีโอถ้ากำลังบันทึกอยู่
            if self.is_recording and self.out is not None:
                # ตรวจสอบว่าเฟรมถูกอ่านอย่างถูกต้อง
                try:
                    frame_resized = cv2.resize(frame, (self.width, self.height))
                    self.out.write(frame_resized)
                except Exception as e:
                    print(f"ข้อผิดพลาดในการบันทึกเฟรม: {e}")
                
            # ปรับขนาดเฟรมให้เป็น 640x480
            resized_frame = cv2.resize(frame, (640, 480))
            # แปลงสีจาก BGR (OpenCV) เป็น RGB สำหรับแสดงผล
            rgb_image_display = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image_display.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image_display.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
            # ส่งสัญญาณภาพที่ได้ไปยัง DisplayWidget
            self.frame_received.emit(qt_image)

            # อัปเดตเวลาที่บันทึก
            if self.is_recording and self.start_time:
                elapsed_time = time.time() - self.start_time
                self.time_updated.emit(self.format_time(elapsed_time))

    def format_time(self, elapsed_time):
        mins, secs = divmod(int(elapsed_time), 60)
        millis = int((elapsed_time - int(elapsed_time)) * 1000)
        return f"{mins:02}:{secs:02}.{millis:03}"  # แสดงมิลลิวินาที


class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recording App")

        # ตั้งค่า path เริ่มต้น
        self.save_folder = "video_output"
        if not os.path.exists(self.save_folder):
            os.makedirs(self.save_folder)  # สร้างโฟลเดอร์ถ้ายังไม่มี

        # สร้าง QLabel สำหรับแสดงผลวีดีโอ
        self.label = QLabel()
        self.label.setFixedSize(640, 480)

        # สร้างปุ่ม Start/Stop Recording
        self.record_button = QPushButton("เริ่มบันทึก")
        self.record_button.clicked.connect(self.toggle_recording)

        # สร้าง QLabel สำหรับแสดงเวลา
        self.time_label = QLabel("00:00.000")

        # ปุ่มเลือกที่เก็บไฟล์
        self.select_folder_button = QPushButton("เลือกที่เก็บไฟล์")
        self.select_folder_button.clicked.connect(self.select_save_location)

        # ปุ่มเปิดโฟลเดอร์ที่บันทึกวิดีโอ
        self.open_folder_button = QPushButton("เปิดที่เก็บไฟล์")
        self.open_folder_button.clicked.connect(self.open_save_location)

        # จัดเรียง Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.time_label)
        button_layout.addWidget(self.select_folder_button)
        button_layout.addWidget(self.open_folder_button)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addLayout(button_layout)
        self.setLayout(layout)

        # สร้างและเริ่มต้น VideoCaptureThread
        self.video_thread = VideoCaptureThread()
        self.video_thread.frame_received.connect(self.update_frame)
        self.video_thread.time_updated.connect(self.update_time)
        self.video_thread.start()  # เริ่มต้น VideoCaptureThread

        # ตั้งค่าสถานะการบันทึก
        self.is_recording = False

    def toggle_recording(self):
        if not self.is_recording:
            # ตั้งชื่อไฟล์ตามวันที่และเวลา
            current_time = time.strftime("%Y%m%d_%H%M%S")
            save_path = os.path.join(self.save_folder, f"video_{current_time}.mp4")
            self.video_thread.start_recording(save_path)
            self.record_button.setText("หยุดบันทึก")
            self.is_recording = True
        else:
            # กดหยุดบันทึก
            self.video_thread.stop_recording()
            self.record_button.setText("เริ่มบันทึก")
            self.time_label.setText("00:00.000")
            self.is_recording = False

    def update_frame(self, qt_image):
        # แสดงภาพที่ได้รับจากกล้อง
        self.label.setPixmap(QPixmap.fromImage(qt_image))

    def update_time(self, time_str):
        # อัปเดตเวลาแสดงผล
        self.time_label.setText(time_str)

    def select_save_location(self):
        # เปิดหน้าต่างเลือกโฟลเดอร์
        folder = QFileDialog.getExistingDirectory(self, "เลือกโฟลเดอร์")
        if folder:
            self.save_folder = folder

    def open_save_location(self):
        # เปิดโฟลเดอร์ที่บันทึกวิดีโอ
        os.startfile(self.save_folder)


    def closeEvent(self, event):
        self.video_thread.stop()  # หยุด Thread เมื่อปิดโปรแกรม
        self.video_thread.wait()  # รอให้เธรดหยุดก่อนที่จะปิดโปรแกรม
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DisplayWidget()
    widget.show()
    sys.exit(app.exec())
