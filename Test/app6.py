# Grid Box Layout
from PyQt6.QtCore import QCoreApplication, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fall Down Detection")
        self.setFixedSize(QSize(400, 300))
        
        # สร้าง Layout และตั้งค่า
        grid = QGridLayout(self)
        # self.setLayout(grid)
        
        # button widget
        btn1 = QPushButton("1")
        btn2 = QPushButton("2")
        btn3 = QPushButton("3")
        btn4 = QPushButton("4")
        
        # จัดวาง widget ใน layout 
        grid.addWidget(btn1, 0, 0)
        grid.addWidget(btn2, 0, 1)
        grid.addWidget(btn3, 1, 0)
        grid.addWidget(btn4, 1, 1)
        
        
app = QCoreApplication.instance()
if app is None:
    app = QApplication([])
    
window = MainWindow()
window.show()
app.exec()