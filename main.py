import sys
# sys ใช้สำหรับบางคำสั่งหรือบาง argv และเพื่อต้องการจัดการกับ Command-Line
from PyQt6.QtWidgets import (
    QApplication, QWidget, QMessageBox , 
    QPushButton, QMainWindow,
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
        
        # setting geometry 
        self.setGeometry(100, 100, 600, 400) 
  
        # calling method 
        self.UiComponents() 
  
        # showing all the widgets 
        self.show() 
  
    # method for widgets 
    def UiComponents(self): 
  
        # creating a push button 
        button1 = QPushButton("First", self) 
  
        # setting geometry of button 
        button1.setGeometry(200, 150, 100, 40) 
  
        # adding action to a button 
        button1.clicked.connect(self.clickme) 
  
        # creating a push button 
        button2 = QPushButton("Second", self) 
  
        # setting geometry of button 
        button2.setGeometry(210, 160, 100, 40) 
  
        # adding action to a button 
        button2.clicked.connect(self.clickme) 
  
        # make it in lower the window 
        button2.lower() 
  
  
    # action method 
    def clickme(self): 
  
  
        # printing pressed 
        print("pressed") 
        
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
