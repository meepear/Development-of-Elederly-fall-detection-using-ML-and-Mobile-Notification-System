# จัดการ Widget ด้วย Medthod
from PyQt6.QtCore import QCoreApplication, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fall Down Detection")
        self.setFixedSize(QSize(400, 300))
        
        # สร้าง Layout และตั้งค่า
        vbox = QVBoxLayout()
        self.setLayout(vbox)
        
        for message in ["Open", "Save", "Exit"]:
            self.display_button(message, vbox)
        
        
    def display_button(self, text, layout):
        btn = QPushButton(text)
        btn.setFixedSize(QSize(100, 50))
        layout.addWidget(btn)

        
        
app = QCoreApplication.instance()
if app is None:
    app = QApplication([])
    
window = MainWindow()
window.show()
app.exec()