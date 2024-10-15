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
    (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8),
    (9, 10), (11, 12), (12, 24), (24, 23), (23, 11),
    (11, 13), (13, 15), (12, 14), (14, 16),
    (15, 17), (15, 21), (15, 19), (19, 17),
    (16, 18), (16, 22), (16, 20), (20, 18),
    (23, 25), (25, 27), (27, 29), (29, 31), (31, 27),
    (24, 26), (26, 28), (28, 30), (30, 32), (28, 32)
]

# Step 3: คำนวณอัตราการเคลื่อนไหวจากการเชื่อมต่อจุด
movement_rates = []

for i in range(len(df)):
    frame = df.iloc[i]
    total_distance = 0
    for connection in connections:
        PosePrevious, PoseCurent = connection
        dx = frame[f'x{PoseCurent}'] - frame[f'x{PosePrevious}']
        dy = frame[f'y{PoseCurent}'] - frame[f'y{PosePrevious}']
        dz = frame[f'z{PoseCurent}'] - frame[f'z{PosePrevious}']
        distance = np.sqrt(dx**2 + dy**2 + dz**2)  # คำนวณระยะทาง
        total_distance += distance
    movement_rates.append(total_distance)

# *******************************แก้
# Step 4: คำนวณอัตราการเคลื่อนไหวใน 1 วินาที (60 เฟรม)
movement_rates_per_second = []
for i in range(0, len(movement_rates), 60):
    if i + 60 <= len(movement_rates):
        movement_sum = np.sum(movement_rates[i:i + 60])
        movement_rates_per_second.append(movement_sum)

# Step 5: คำนวณส่วนต่างอัตราการเคลื่อนไหวระหว่าง 1 วินาทีต่อไป
rate_of_change_diff = []
for i in range(1, len(movement_rates_per_second)):
    diff = np.abs(movement_rates_per_second[i] - movement_rates_per_second[i-1])  # หาส่วนต่าง
    rate_of_change_diff.append(diff)

# Step 6: สร้างกราฟแสดงอัตราการเคลื่อนไหวใน 1 วินาที
plt.figure(figsize=(12, 6))
plt.plot(range(len(movement_rates_per_second)), movement_rates_per_second, marker='o', label='Total Movement Rate per Second')
plt.title('Total Movement Rate in 1 Second (60fps)')
plt.xlabel('Second Index')
plt.ylabel('Total Movement Distance')
plt.legend()
plt.grid()
plt.show()

# Step 7: สร้างกราฟแสดงส่วนต่างอัตราการเคลื่อนไหว
plt.figure(figsize=(12, 6))
plt.plot(range(1, len(rate_of_change_diff) + 1), rate_of_change_diff, marker='o', color='r', label='Rate of Change Difference per Second')
plt.title('Rate of Change Difference Between Seconds')
plt.xlabel('Second Index')
plt.ylabel('Difference in Movement Rate')
plt.legend()
plt.grid()
plt.show()
