from PyQt6.QtWidgets import QApplication, QWidget

# สร้าง Application
app = QApplication([])
# สร้าง Widget หน้าต่าง
window = QWidget()
# เรียกใช้งานหน้าต่าง
window.show()

# เรียกใช้งาน Application
app.exec()