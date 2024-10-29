import pandas as pd
import numpy as np
import os

# ฟังก์ชันหลักที่ทำงานตามที่อธิบาย
def calculate_rates():
    # อ่านไฟล์ CSV
    file_name = 'walk-sit.csv'
    csv_path = os.path.join('csv', file_name)
    
    data = pd.read_csv(csv_path)
    
    # กำหนดลิสต์เพื่อเก็บค่าผลลัพธ์
    frame_rates = []
    angular_velocities = []
    movement_rates = []

    # # กำหนดจุดที่เชื่อมต่อสำหรับ Movement Rate
    connections = [(11, 12), (12, 24), (24, 23), (23, 11), 
                   (15, 13), (13, 11), (12, 14), (14, 16), 
                   (23, 25), (25, 27), (24, 26), (26, 28)]

    # คำนวณค่าตามจำนวนเฟรมที่มี
    for n in range(1, len(data) - 1):  # เฟรมเริ่มจาก 1 ถึง len(data) - 2
        # คำนวณ Frame Rate
        image_timestamp_n = data['Image_Timestamp'][n]
        pose_timestamp_n = data['Pose_Timestamp'][n]
        image_timestamp_n1 = data['Image_Timestamp'][n + 1]
        pose_timestamp_n1 = data['Pose_Timestamp'][n + 1]
        
        frame_diff_n = abs(image_timestamp_n - pose_timestamp_n)
        frame_diff_n1 = abs(image_timestamp_n1 - pose_timestamp_n1)
        frame_rate = abs(frame_diff_n - frame_diff_n1)
        frame_rate = 1

        frame_rates.append(frame_rate)
        
        # คำนวณ Angular Velocity
        cog_x_n = (data.iloc[n, 24] + data.iloc[n, 23]) / 2
        cog_y_n = (data.iloc[n, 24 + 1] + data.iloc[n, 23 + 1]) / 2
        cog_x_n1 = (data.iloc[n + 1, 24] + data.iloc[n + 1, 23]) / 2
        cog_y_n1 = (data.iloc[n + 1, 24 + 1] + data.iloc[n + 1, 23 + 1]) / 2
        
        dy_n = cog_y_n - data.iloc[n, 0]  # y ของตำแหน่งที่ 0
        dx_n = cog_x_n - data.iloc[n, 0]  # x ของตำแหน่งที่ 0
        
        dy_n1 = cog_y_n1 - data.iloc[n + 1, 0]
        dx_n1 = cog_x_n1 - data.iloc[n + 1, 0]
        
        angle_n = np.arctan2(dy_n, dx_n) * 180 / np.pi
        angle_n1 = np.arctan2(dy_n1, dx_n1) * 180 / np.pi
        
        # angular_velocity = abs(angle_n1 - angle_n) / frame_rate if frame_rate != 0 else 0
        angular_velocity = (angle_n1) / frame_rate if frame_rate != 0 else 0
        angular_velocities.append(angular_velocity)
        
        # คำนวณ Movement Rate
        total_length_n = 0
        total_length_n1 = 0
        
        for connection in connections:
            point_a_n = data.iloc[n , connection[0]]
            point_b_n = data.iloc[n, connection[1]]
            total_length_n += np.sqrt(((point_a_n - point_b_n) ** 2) + ((data.iloc[n, connection[0] + 1] - data.iloc[n, connection[1] + 1]) ** 2))
            
            point_a_n1 = data.iloc[n + 1, connection[0]]
            point_b_n1 = data.iloc[n + 1, connection[1]]
            total_length_n1 += np.sqrt((point_a_n1 - point_b_n1) ** 2 + (data.iloc[n + 1, connection[0] + 1] - data.iloc[n + 1, connection[1] + 1]) ** 2)
        
        if n > 0:
            movement_rate_n = np.sqrt((((total_length_n - total_length_n1) ** 2) / 1920) + (((total_length_n - total_length_n1) ** 2) / 1080)) / frame_rate
        else:
            movement_rate_n = 0
            
        movement_rates.append(movement_rate_n)

    # สร้าง DataFrame สำหรับผลลัพธ์
    result_df = pd.DataFrame({
        'Frame_Rate': frame_rates,
        'Angular_Velocity': angular_velocities,
        'Movement_Rate': movement_rates
    })

    # บันทึกผลลัพธ์ลงใน CSV
    output_csv_path = os.path.join('csv', 'data_fall.csv')
    if os.path.exists(output_csv_path):
        result_df.to_csv(output_csv_path, mode='a', header=False, index=False)
    else:
        result_df.to_csv(output_csv_path, index=False)

# เรียกใช้งานฟังก์ชัน
calculate_rates()
