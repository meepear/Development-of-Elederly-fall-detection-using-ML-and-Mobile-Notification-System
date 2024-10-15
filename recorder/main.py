import sys
import cv2
import time
import os
import pandas as pd 
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
        self.landmarks_data = []  # สร้างลิสต์เพื่อเก็บข้อมูล landmark
        
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

    def start_recording(self, save_vdo_path, save_csv_path):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(save_vdo_path, fourcc, self.fps, (self.width, self.height)) 
        self.start_time = time.time()  # เก็บเวลาที่เริ่มต้น
        self.is_recording = True
        
        # เตรียมข้อมูลสำหรับ CSV
        self.landmarks_data = []  # ล้างข้อมูลเดิม
        self.csv_path = save_csv_path  # เก็บ path ของไฟล์ CSV
        
        # เขียนหัวข้อคอลัมน์ในไฟล์ CSV
        self.columns = ["frames", 'frame_time', 'pose_time',
                        "x0", "y0", "z0",
                        "x1", "y1", "z1", 
                        "x2", "y2", "z2", 
                        "x3", "y3", "z3", 
                        "x4", "y4", "z4", 
                        "x5", "y5", "z5", 
                        "x6", "y6", "z6", 
                        "x7", "y7", "z7", 
                        "x8", "y8", "z8", 
                        "x9", "y9", "z9", 
                        "x10", "y10", "z10", 
                        "x11", "y11", "z11", 
                        "x12", "y12", "z12", 
                        "x13", "y13", "z13", 
                        "x14", "y14", "z14", 
                        "x15", "y15", "z15", 
                        "x16", "y16", "z16", 
                        "x17", "y17", "z17", 
                        "x18", "y18", "z18", 
                        "x19", "y19", "z19", 
                        "x20", "y20", "z20", 
                        "x21", "y21", "z21", 
                        "x22", "y22", "z22", 
                        "x23", "y23", "z23", 
                        "x24", "y24", "z24", 
                        "x25", "y25", "z25", 
                        "x26", "y26", "z26", 
                        "x27", "y27", "z27", 
                        "x28", "y28", "z28", 
                        "x29", "y29", "z29", 
                        "x30", "y30", "z30", 
                        "x31", "y31", "z31", 
                        "x32", "y32", "z32"]
        # เขียนหัวข้อคอลัมน์ลงไฟล์ CSV
        pd.DataFrame(columns=self.columns).to_csv(self.csv_path, index=False)

    def stop_recording(self):
        if self.out is not None:
            self.out.release() 
        self.is_recording = False
        self.start_time = None
        
        # บันทึกข้อมูลลง CSV
        if self.landmarks_data:
            df = pd.DataFrame(self.landmarks_data, columns=self.columns)  # ใช้ชื่อคอลัมน์ที่กำหนด
            df.to_csv(self.csv_path, index=False, mode='a', header=False)  # append ข้อมูลลงใน CSV

    def stop(self):
        self.running = False

    def run(self):
        frame_count = 0  # ตัวนับเฟรม
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
                    
                    # ดำเนินการตรวจจับ landmark ที่นี่
                    frame_data = self.detect_landmarks(frame, frame_count)  # เรียกฟังก์ชันเพื่อตรวจจับ landmark
                    if frame_data is not None:
                        self.landmarks_data.append(frame_data)  # บันทึกข้อมูล landmark ลงในลิสต์
                        frame_count += 1  # เพิ่มตัวนับเฟรม
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
    
    def detect_landmarks(self, frame, frame_count):
        landmarks = [0.0] * 99 
        
        # สร้างข้อมูลที่จะบันทึก
        frame_time = self.format_time(time.time() - self.start_time)  # เวลาที่เฟรมถูกสร้าง
        pose_time = self.format_time(frame_count / self.fps)  # เวลาที่ pose ถูกสร้าง
        
        # บันทึกข้อมูล timestamp และ landmark ลงในลิสต์
        return [frame_count, frame_time, pose_time] + landmarks  # รวมข้อมูลในรูปแบบที่ต้องการ


class DisplayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Recording App")

        # ตั้งค่า path เริ่มต้น
        self.output_folders = ['csv', 'vdo']
        for folder in self.output_folders:
            os.makedirs(folder, exist_ok=True)
        self.csv_output = self.output_folders[0]
        self.vdo_output = self.output_folders[1]

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

        # สร้าง VideoCaptureThread
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
            save_vdo_path = os.path.join(self.vdo_output, f"{current_time}.mp4")
            save_csv_path = os.path.join(self.csv_output, f"{current_time}.csv")
            self.video_thread.start_recording(save_vdo_path, save_csv_path)
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
            self.vdo_output = folder

    def open_save_location(self):
        # เปิดโฟลเดอร์ที่บันทึกวิดีโอ
        os.startfile(self.vdo_output)


    def closeEvent(self, event):
        self.video_thread.stop()  # หยุด Thread เมื่อปิดโปรแกรม
        self.video_thread.wait()  # รอให้เธรดหยุดก่อนที่จะปิดโปรแกรม
        event.accept()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DisplayWidget()
    widget.show()
    sys.exit(app.exec())
