import sys
# sys ใช้สำหรับบางคำสั่งหรือบาง argv และเพื่อต้องการจัดการกับ Command-Line
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMessageBox , 
    QPushButton, QMainWindow, QMessageBox,
    QVBoxLayout, QLabel, QLineEdit,
    QGridLayout)
# QApplication เป็นตัวจัดการ application และจัดการ QWidget
# QWidget คือ เป็นคลาสพื้นฐานสำหรับทุก widget ใน PyQt ทำหน้าที่เป็นคอนเทนเนอร์สำหรับวาง widgets
# QPushButton เป็น Widget ปุ่มกด
# QMainWindow เอามาเพื่อสร้างคลาสย่อยเพื่อเพิ่มอิสระในการทำงานของโปรแกรม
from PyQt6.QtCore import QSize, Qt # เกี่ยวกับขนาด
from PyQt6.QtGui import QPalette, QColor # การจัดวาง Layout

class MainWindow(QMainWindow):
    def __init__(self): # เป็นฟังก์ชันที่ใช้สำหรับกำหนดค่าหรือเตรียมการก่อนที่ออบเจ็กต์จะถูกสร้างขึ้น
        super().__init__()
        self.setWindowTitle("Fall Down Program") # ตั้งชื่อให้กับ Widget
        # self.showFullScreen()
        self.resize(1600, 900)
        
        # สร้าง central widget และ layout หลัก
        self.central_widget = QWidget()
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        self.setCentralWidget(self.central_widget)

        # สร้างปุ่ม
        self.button = QPushButton("Click")
        self.button.clicked.connect(self.show_input_layout)
        
        # เพิ่มปุ่มลงใน layout
        self.main_layout.addWidget(self.button)

    def show_input_layout(self):
        # สร้าง layout ใหม่
        input_layout = QGridLayout()
        
        # สร้าง QLabel และ QLineEdit
        label = QLabel("What is your name?")
        self.line_edit = QLineEdit()
        
        # เพิ่ม widget ลงใน layout
        input_layout.addWidget(label, 0, 0)  # เพิ่ม label ที่แถวที่ 0, คอลัมน์ที่ 0
        input_layout.addWidget(self.line_edit, 1, 0)  # เพิ่ม QLineEdit ที่แถวที่ 1, คอลัมน์ที่ 0
        
        # ล้าง layout หลักก่อนเพิ่ม layout ใหม่
        while self.main_layout.count():
            child = self.main_layout.itemAt(0)
            if child.widget():
                child.widget().deleteLater()
            else:
                child.layout().deleteLater()
        
        # เพิ่ม layout ใหม่ลงใน layout หลัก
        self.main_layout.addLayout(input_layout)
        
    # Function ตรวจสอบการกดปุ่ม
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape: # ESC
            self.showNormal()  # กลับไปที่หน้าต่างขนาดปกติ
            self.resize(1600, 900)
        elif event.key() == Qt.Key.Key_F: # F
            self.showFullScreen()  # กลับไปที่หน้าต่างเต็มจอ


app = QApplication(sys.argv) # สร้าง application ด้วย QApplication
window = MainWindow() # สร้าง Widget เปล่าขึ้นมาด้วย QWidget เป็นหน้าต่างของโปรแกรม
window.show() # ให้แสดง Widget หน้าต่างของโปแกรม
app.exec() # เริ่มใช้ event loop เพื่อใช้งาน Widget ต่างในโปแกรม
