import pandas as pd
import numpy as np
import os

# ฟังก์ชันหลักที่ทำงานตามที่อธิบาย
def calculate_rates():
    # อ่านไฟล์ CSV
    file_name = input('File CSV name: ')
    file_path = f'{file_name}.csv'
    csv_path = os.path.join('csv', file_path)
    
    data = pd.read_csv(csv_path)
    
    # กำหนดลิสต์เพื่อเก็บค่าผลลัพธ์
    frame_rates = []
    cog_angles = []
    movement_rates = []
    
    # กำหนดค่า threshold สำหรับ frame_rate ที่น้อยที่สุด
    frame_rate_threshold = 0.0039
    
    skipped_frames = []  # เก็บเฟรมที่ข้าม

    # # กำหนดจุดที่เชื่อมต่อสำหรับ Movement Rate
    connections = [(0, 11), (11, 12), (12, 24), (24, 23), (23, 11), 
                   (15, 13), (13, 11), (12, 14), (14, 16), 
                   (23, 25), (25, 27), (24, 26), (26, 28)]

    # คำนวณค่าตามจำนวนเฟรมที่มี n เป็นเฟรมก่อนหน้า n + 1 เฟรมปัจจุบัน
    for n in range(len(data) - 1):  # เฟรมเริ่มจาก 0 ถึง len(data) - 2
        # คำนวณ Frame Rate
        image_timestamp_n = data['Image_Timestamp'][n]
        pose_timestamp_n = data['Pose_Timestamp'][n]
        if n + 1 < len(data):
            image_timestamp_n1 = data['Image_Timestamp'][n + 1]  # เฟรมปัจจุบัน
            pose_timestamp_n1 = data['Pose_Timestamp'][n + 1]  # เฟรมปัจจุบัน
            
            frame_diff_n = abs(image_timestamp_n - pose_timestamp_n)
            frame_diff_n1 = abs(image_timestamp_n1 - pose_timestamp_n1)  # เฟรมปัจจุบัน
            frame_rate = abs(frame_diff_n - frame_diff_n1)
        else:
            frame_rate = 0  # กำหนดค่าเป็น 0 สำหรับเฟรมสุดท้ายที่ไม่มีการคำนวณ

        # ตรวจสอบ frame_rate น้อยกว่า threshold
        if frame_rate < frame_rate_threshold:
            skipped_frames.append(n)  
            frame_rates.append(0)  # บันทึก 0 แทนเฟรมที่ข้าม
            cog_angles.append(0)  # บันทึก 0 สำหรับมุม COG
            movement_rates.append(0)  # บันทึก 0 สำหรับ Movement Rate
            continue  

        frame_rates.append(frame_rate)
        
        # คำนวณ Center of Gravity Angle
        cog_x_n1 = (data.iloc[n + 1, 24] + data.iloc[n + 1, 23]) / 2
        cog_y_n1 = (data.iloc[n + 1, 24 + 1] + data.iloc[n + 1, 23 + 1]) / 2
        
        dx_n1 = cog_x_n1 - data.iloc[n + 1, 0]  # x ของตำแหน่งอ้างอิงที่เฟรม ปัจจุบัน
        dy_n1 = cog_y_n1 - data.iloc[n + 1, 0]  # y ของตำแหน่งอ้างอิงที่เฟรม ปัจจุบัน
        
        # คำนวณมุม COG ในเฟรม ปัจจุบัน
        angle_n1 = np.arctan2(dy_n1, dx_n1) * 180 / np.pi

        cog_angles.append(angle_n1)
        
        # คำนวณ Movement Rate
        total_length_n = 0
        total_length_n1 = 0
        
        for connection in connections:
            point_a_n = data.iloc[n, connection[0]]
            point_b_n = data.iloc[n, connection[1]]
            total_length_n += np.sqrt(((point_a_n - point_b_n) ** 2) + ((data.iloc[n, connection[0] + 1] - data.iloc[n, connection[1] + 1]) ** 2))
            
            if n + 1 < len(data):
                point_a_n1 = data.iloc[n + 1, connection[0]]
                point_b_n1 = data.iloc[n + 1, connection[1]]
                total_length_n1 += np.sqrt((point_a_n1 - point_b_n1) ** 2 + (data.iloc[n + 1, connection[0] + 1] - data.iloc[n + 1, connection[1] + 1]) ** 2)
            else:
                total_length_n1 += 0  # กำหนดเป็น 0 ถ้าไม่มีเฟรมถัดไป

        movement_rate_n = np.sqrt((((total_length_n - total_length_n1) ** 2) / 1920) + (((total_length_n - total_length_n1) ** 2) / 1080)) / frame_rate

        movement_rates.append(movement_rate_n)

    # สรุปการข้ามเฟรม
    print("\nSummary of skipped frames due to low frame_rate:")
    print(", ".join(map(str, skipped_frames)))

    # สร้าง DataFrame สำหรับผลลัพธ์
    result_df = pd.DataFrame({
        'Frame_Rate': frame_rates,
        'CoG_Angles': cog_angles,
        'Movement_Rate': movement_rates
    })

    # บันทึกผลลัพธ์ลงใน CSV
    output_csv_path = os.path.join('csv', f'Data_{file_path}')
    if os.path.exists(output_csv_path):
        result_df.to_csv(output_csv_path, mode='a', header=False, index=False)
    else:
        result_df.to_csv(output_csv_path, index=False)

# เรียกใช้งานฟังก์ชัน
calculate_rates()
