import sys, cv2, time, os
from PyQt6.QtCore import QThread, pyqtSignal
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget, QPushButton, QHBoxLayout

# คลาสสำหรับ Video ที่แสดงบนโปรแกรม
class VideoCaptureThread(QThread):
    # Signal ที่ใช้แสดง Video บนโปรแกรม
    frame_received = pyqtSignal(QImage)
    time_updated = pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
        self.cap = cv2.VideoCapture(0)
        self.running = True         # ให้เปิดกล้องเมื่อเริ่มโปรแกรม
        self.out_video = None       # การเขียนบันทึก Video
        self.is_recording = False
        
        # >-------- ปรับความละเอียดในการบันทึกวีดีโอ --------<
        WIDTH = 1280
        HEIGHT = 720
        FPS = 30
        
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
        self.cap.set(cv2.CAP_PROP_FPS, FPS)
        
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = self.cap.get(cv2.CAP_PROP_FPS)
        
        # >------------------ END ------------------<
        
        

    def start_recording(self, save_vdo_path, save_csv_path):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out_video = cv2.VideoWriter(save_vdo_path, fourcc, self.fps, (self.width, self.height)) 
        self.start_time = time.time()  # เก็บเวลาที่เริ่มต้น
        self.is_recording = True
    
        
    def stop_recording(self):
        if self.out_video is not None:
            self.out_video.release() 
        self.is_recording = False
        self.start_time = None
        
            
    def stop(self):
        self.running = False
    
    def run(self):
        while self.running:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # แปลงสีจาก BGR (OpenCV) เป็น RGB สำหรับแสดงผล
            rgb_image_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            if self.is_recording and self.out_video is not None:
                # บันทึกเฟรมปัจจุบันลงในไฟล์วิดีโอ
                self.out_video.write(frame)
                

            # ปรับขนาดเฟรมให้เป็น 640x480
            resized_frame = cv2.resize(rgb_image_display, (640, 480))
            h, w, ch = resized_frame.shape
            bytes_per_line = ch * w
            qt_image = QImage(resized_frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)
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
    

# ------------------------ Display ------------------------
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

        # ปุ่มเปิดโฟลเดอร์ที่บันทึกวิดีโอ
        self.open_folder_button = QPushButton("เปิดที่เก็บไฟล์")
        self.open_folder_button.clicked.connect(self.open_save_location)

        # จัดเรียง Layout
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.record_button)
        button_layout.addWidget(self.time_label)
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

    def open_save_location(self):
        # เปิดโฟลเดอร์ที่บันทึกวิดีโอ
        os.startfile(self.vdo_output)

    def closeEvent(self, event):
        self.video_thread.stop()  # หยุด Thread เมื่อปิดโปรแกรม
        self.video_thread.wait()  # รอให้เธรดหยุดก่อนที่จะปิดโปรแกรม
        event.accept()
# ------------------------ End Class Display ------------------------

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DisplayWidget()
    widget.show()
    sys.exit(app.exec())
