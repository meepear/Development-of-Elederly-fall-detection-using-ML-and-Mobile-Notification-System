import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Step 1: อ่านข้อมูลจากไฟล์ CSV
file_name = 'sit-stand-walk-sleep'
file_dir = f'motion-detection/{file_name}.csv'  # แทนที่ด้วยชื่อไฟล์ของคุณ
df = pd.read_csv(file_dir)

# *******************************แก้ เอาเฉพาะลำตัวแขนขาไม่เอานิ้ว ใบหน้าเอาแค่จมูก
# Step 2: เชื่อมต่อจุดต่าง ๆ ตามที่กำหนด
connections = [
                (11, 12), (12, 24), (24, 23), (23, 11),
                (15, 13), (13, 11), (12, 14), (14, 16),
                (23, 25), (25, 27), (24, 26), (26, 28)
                ]

# Step 3: คำนวณอัตราการเคลื่อนไหวจากการเชื่อมต่อจุด
movement_rate_area = []

for i in range(len(df)):
    frame = df.iloc[i]
    total_distance = 0
    for connection in connections:
        PosePrevious, PoseCurent = connection
        dx = frame[f'x{PoseCurent}'] - frame[f'x{PosePrevious}']
        dy = frame[f'y{PoseCurent}'] - frame[f'y{PosePrevious}']
        distance = np.sqrt(dx**2 + dy**2)  # คำนวณระยะทาง
        total_distance += distance
    movement_rate_area.append(total_distance)