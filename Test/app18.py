# CheckBox
from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QPixmap

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
        
        # img = QPixmap("ที่อยู่รูปภาพ")
        # label = QLabel()
        # label.setPixmap(img)
        # label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        # vbox.addWidget(label)
        
        
        lb = QLabel("Hello User")
        vbox.addWidget(lb)
        
        self.check_person = QCheckBox("Person")
        self.lbStatus = QLabel("Status")
        vbox.addWidget(self.check_person)
        vbox.addWidget(self.lbStatus)
        self.check_person.stateChanged.connect(self.checkStatus)
        
        for message in ["Open", "Save", "Exit"]:
            self.display_button(message, vbox)
        
        
    def display_button(self, text, layout):
        btn = QPushButton(text)
        btn.setFixedSize(QSize(100, 50))
        layout.addWidget(btn)
        
        # เชื่อมต่อปุ่ม(Signal) กับ Slot 
        if text == "Open":
            btn.clicked.connect(self.open_action)
        elif text == "Save":
            btn.clicked.connect(self.save_action)
        elif text == "Exit":
            btn.clicked.connect(self.exit_action)
            
    def open_action(self):
        print("Open button clicked")
        sender = self.sender()
        print(sender.text())


    def save_action(self):
        print("Save button clicked")

    def exit_action(self):
        print("Exit button clicked")
        QApplication.quit()  # ปิดแอพพลิเคชัน
        
    def checkStatus(self):
        sender = self.sender()
        self.lbStatus.setText(sender.text()+" : "+str(sender.isChecked()))
        
        items=[]
        if sender.text() == "Person":
            items.append(sender.text())
        
        text = "List\n"+", ".join(items)
        # QMessageBox.information(self, "แจ้งเตือน", text)
            
        
        
app = QCoreApplication.instance()
if app is None:
    app = QApplication([])
    with open('Test/style.qss', 'r') as style:
        app.setStyleSheet(style.read())
    
window = MainWindow()
window.show()
app.exec()