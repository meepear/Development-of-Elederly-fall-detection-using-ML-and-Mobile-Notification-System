# alignment & spacing
from PyQt6.QtCore import QCoreApplication, QSize, Qt
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fall Down Detection")
        self.setFixedSize(QSize(800, 600))
        
        # สร้าง Layout และตั้งค่า
        vbox = QVBoxLayout()
        vbox.setAlignment(Qt.AlignmentFlag.AlignTop)
        vbox.setSpacing(10)
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