# Vertical Box Layout
from PyQt6.QtCore import QCoreApplication
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fall Down Detection")
        
        # สร้าง Layout และตั้งค่า
        vbox = QVBoxLayout(self)
        self.setLayout(vbox)
        
        # button widget
        btn1 = QPushButton("1")
        btn2 = QPushButton("2")
        btn3 = QPushButton("3")
        
        # จัดวาง widget ใน layout 
        vbox.addWidget(btn1)
        vbox.addWidget(btn2)
        vbox.addWidget(btn3)
        
        
app = QCoreApplication.instance()
if app is None:
    app = QApplication([])
    
window = MainWindow()
window.show()
app.exec()