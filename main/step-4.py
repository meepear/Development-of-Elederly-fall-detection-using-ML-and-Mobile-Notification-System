import pandas as pd
import numpy as np
import os
import cv2
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.spatial import distance

# ฟังก์ชันที่ใช้ในการคำนวณค่าต่างๆ
def calculate_rates(data, frame_idx, frame_rate):
    angular_velocity = 0
    movement_rate = 0

    # เช็คจำนวนเฟรมเพียงพอหรือไม่
    if frame_idx < 1 or frame_idx >= len(data) - 1:
        return angular_velocity, movement_rate

    # กำหนดจุดเชื่อมต่อ skeleton
    connections = [(11, 12), (12, 24), (24, 23), (23, 11), 
                   (15, 13), (13, 11), (12, 14), (14, 16), 
                   (23, 25), (25, 27), (24, 26), (26, 28)]
    
    # คำนวณ Center of Gravity (CoG)
    cog_x_n = (data.iloc[frame_idx, 24] + data.iloc[frame_idx, 23]) / 2
    cog_y_n = (data.iloc[frame_idx, 24 + 1] + data.iloc[frame_idx, 23 + 1]) / 2
    cog_x_n1 = (data.iloc[frame_idx + 1, 24] + data.iloc[frame_idx + 1, 23]) / 2
    cog_y_n1 = (data.iloc[frame_idx + 1, 24 + 1] + data.iloc[frame_idx + 1, 23 + 1]) / 2
    
    # คำนวณมุมของจุด CoG แต่ละเฟรม
    dy_n = cog_y_n - data.iloc[frame_idx, 0]
    dx_n = cog_x_n - data.iloc[frame_idx, 0]
    dy_n1 = cog_y_n1 - data.iloc[frame_idx + 1, 0]
    dx_n1 = cog_x_n1 - data.iloc[frame_idx + 1, 0]
    
    angle_n = np.arctan2(dy_n, dx_n) * 180 / np.pi
    angle_n1 = np.arctan2(dy_n1, dx_n1) * 180 / np.pi
    angular_velocity = abs(angle_n1 - angle_n) / frame_rate if frame_rate != 0 else 0

    # คำนวณ Movement Rate
    total_length_n = 0
    total_length_n1 = 0
    for connection in connections:
        point_a_n = data.iloc[frame_idx, connection[0]]
        point_b_n = data.iloc[frame_idx, connection[1]]
        point_a_n1 = data.iloc[frame_idx + 1, connection[0]]
        point_b_n1 = data.iloc[frame_idx + 1, connection[1]]
        
        total_length_n += distance.euclidean((point_a_n, data.iloc[frame_idx, connection[0] + 1]), 
                                             (point_b_n, data.iloc[frame_idx, connection[1] + 1]))
        total_length_n1 += distance.euclidean((point_a_n1, data.iloc[frame_idx + 1, connection[0] + 1]), 
                                              (point_b_n1, data.iloc[frame_idx + 1, connection[1] + 1]))
        
    movement_rate = np.sqrt(((total_length_n - total_length_n1) ** 2) / 1920 + 
                            ((total_length_n - total_length_n1) ** 2) / 1080) / frame_rate

    return angular_velocity, movement_rate

# แสดงผลแบบเรียลไทม์จากกล้อง
def realtime_display():
    # โหลดไฟล์ CSV
    file_name = 'pun_walk_back_1.csv'
    csv_path = os.path.join('csv', file_name)
    data = pd.read_csv(csv_path)

    # เปิดกล้อง
    cap = cv2.VideoCapture(0)
    frame_idx = 0
    frame_rate = 1  # ตั้งค่าเฟรมเรทให้เป็น 1 เนื่องจากคำนวณแบบเฟรมต่อเฟรม

    # สร้างกราฟแบบเรียลไทม์
    fig, (ax1, ax2) = plt.subplots(2, 1)
    angular_velocities = []
    movement_rates = []
    frames = []

    def update_plot(i):
        nonlocal frame_idx
        ret, frame = cap.read()
        if not ret:
            return

        angular_velocity, movement_rate = calculate_rates(data, frame_idx, frame_rate)
        angular_velocities.append(angular_velocity)
        movement_rates.append(movement_rate)
        frames.append(frame_idx)

        # ลบเส้นกราฟเก่าก่อนอัพเดตเส้นกราฟใหม่
        ax1.clear()
        ax2.clear()
        ax1.plot(frames, angular_velocities, 'b-')
        ax1.set_title('Angular Velocity')
        ax2.plot(frames, movement_rates, 'r-')
        ax2.set_title('Movement Rate')

        # วาด skeleton บนภาพ
        for connection in [(11, 12), (12, 24), (24, 23), (23, 11), 
                           (15, 13), (13, 11), (12, 14), (14, 16), 
                           (23, 25), (25, 27), (24, 26), (26, 28)]:
            point_a = (int(data.iloc[frame_idx, connection[0]]), int(data.iloc[frame_idx, connection[0] + 1]))
            point_b = (int(data.iloc[frame_idx, connection[1]]), int(data.iloc[frame_idx, connection[1] + 1]))
            cv2.line(frame, point_a, point_b, (0, 255, 0), 2)
        
        # แสดงผลภาพ
        cv2.imshow('Skeleton', frame)

        # อัพเดต frame index
        frame_idx += 1
        if frame_idx >= len(data) - 1:
            frame_idx = 0

    # เรียกใช้การอัพเดตแบบเรียลไทม์
    ani = FuncAnimation(fig, update_plot, interval=100)
    plt.show()

    # ปิดกล้องเมื่อจบการทำงาน
    cap.release()
    cv2.destroyAllWindows()

# เรียกฟังก์ชันการแสดงผล
realtime_display()
