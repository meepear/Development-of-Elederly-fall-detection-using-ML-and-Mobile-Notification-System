import pandas as pd
import numpy as np

# Step 1: อ่านข้อมูลจากไฟล์ CSV
file_name = 'pun_walk_front_1'
file_dir = f'csv/{file_name}.csv'
df = pd.read_csv(file_dir)

# คำนวณส่วนต่างของ Image_Timestamp และ Pose_Timestamp
df['Frame_rate'] = abs(df['Image_Timestamp'] - df['Pose_Timestamp'])

# ฟังก์ชันช่วยคำนวณส่วนต่าง x, y
def calc_diff(df, point1, point2):
    diff_x = abs(df[f'x{point2}'] - df[f'x{point1}'])
    diff_y = abs(df[f'y{point2}'] - df[f'y{point1}'])
    return diff_x, diff_y

# Step 2: เชื่อมต่อจุด
connections = [(11, 12), (12, 24), (24, 23), (23, 11),
         (15, 13), (13, 11),
         (12, 14), (14, 16),
         (23, 25), (25, 27),
         (24, 26), (26, 28)]

diff_x_total = []
diff_y_total = []

# Step 3: Diff X และ Y
for point1, point2 in connections:
    diff_x, diff_y = calc_diff(df, point1, point2)
    diff_x_total.append(diff_x)
    diff_y_total.append(diff_y)

# แปลงเป็น DataFrame เพื่อนำไปรวมกับข้อมูลใหม่
diff_x_total = np.sum(diff_x_total, axis=0)
diff_y_total = np.sum(diff_y_total, axis=0)

# หาค่ากึ่งกลางของจุด (23, 24)
midpoint_x = (df['x23'] + df['x24']) / 2
midpoint_y = (df['y23'] + df['y24']) / 2

# คำนวณมุม Degree กับจุดที่ 0 (x0, y0)
def calc_degree(x0, y0, mid_x, mid_y):
    delta_x = mid_x - x0
    delta_y = mid_y - y0
    angle = np.arctan2(delta_y, delta_x)  # ใช้ np.arctan2 สำหรับ Series
    return np.sin(angle)

# เรียกใช้ฟังก์ชัน calc_degree
df['Degree'] = calc_degree(df['x0'], df['y0'], midpoint_x, midpoint_y)

# สร้าง DataFrame ใหม่เพื่อเก็บผลลัพธ์
output_df = pd.DataFrame({
    'Frame_rate': df['Frame_rate'],
    'Diff_x': diff_x_total,
    'Diff_y': diff_y_total,
    'Degree': df['Degree']
})

# บันทึกเป็นไฟล์ CSV ใหม่
output_file = 'csv/movement_walk.csv'
output_df.to_csv(output_file, index=False)

print(f"ผลลัพธ์ถูกบันทึกลงในไฟล์ {output_file} เรียบร้อยแล้ว!")
