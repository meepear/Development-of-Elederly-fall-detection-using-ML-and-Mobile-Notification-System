import os
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from concurrent.futures import ProcessPoolExecutor
from tqdm import tqdm  # ใช้สำหรับ Progress Bar

# อ่านไฟล์ CSV
file_name = 'walk-stand-sleep-sit'
file_path = f'motion-detection/csv/{file_name}.csv'  # กำหนดไฟล์ CSV
if not os.path.exists(file_path):
    raise FileNotFoundError(f"ไม่พบไฟล์: {file_path}")

df = pd.read_csv(file_path)  # อ่านข้อมูลจากไฟล์ CSV

# โฟลเดอร์สำหรับบันทึกภาพกราฟแต่ละเฟรม
output_dir = f'motion-detection/output_frames_Folder/output_frames_{file_name}'
os.makedirs(output_dir, exist_ok=True)
plt.switch_backend('Agg')

# ฟังก์ชันสำหรับการสร้าง skeleton พร้อม grid
def plot_skeleton(frame_data, frame_number, total_frames):
    # *******************************แก้ เอาเฉพาะลำตัวแขนขาไม่เอานิ้ว ใบหน้าเอาแค่จมูก
    connections = [
        (0, 1), (1, 2), (2, 3), (3, 7), (0, 4), (4, 5), (5, 6), (6, 8), 
        (9, 10), (11, 12), (12, 24), (24, 23), (23, 11), 
        (11, 13), (13, 15), (12, 14), (14, 16),
        (15, 17), (15, 21), (15, 19), (19, 17),
        (16, 18), (16, 22), (16, 20), (20, 18),
        (23, 25), (25, 27), (27, 29), (29, 31), (31, 27),
        (24, 26), (26, 28), (28, 30), (30, 32), (28, 32)
    ]
    
    x_vals = np.array([frame_data[f'x{i}'] for i in range(33)])
    y_vals = np.array([frame_data[f'y{i}'] for i in range(33)])
    z_vals = np.array([frame_data[f'z{i}'] for i in range(33)])
    
    # สร้างภาพแบบ subplot ที่มี 2D และ 3D
    fig = plt.figure(figsize=(15, 5))
    
    # วาด 2D skeleton ใน subplot แรก
    ax1 = fig.add_subplot(1, 2, 1)
    ax1.set_title(f'2D Poses at Frame {frame_number}')
    ax1.scatter(x_vals, y_vals, c='green', s=40)  # วาดจุด
    for conn in connections:
        ax1.plot([x_vals[conn[0]], x_vals[conn[1]]], [y_vals[conn[0]], y_vals[conn[1]]], 'r-')  # วาดเส้นเชื่อมต่อ
    ax1.set_xlim(0, 1920)  # ตั้งค่าขนาดแกน x
    ax1.set_ylim(1080, 0)  # ตั้งค่าขนาดแกน y
    ax1.set_xlabel('X')
    ax1.set_ylabel('Y')
    ax1.grid(True)

    # วาด 3D skeleton ใน subplot ที่สอง
    ax2 = fig.add_subplot(1, 2, 2, projection='3d')
    ax2.set_title(f'3D Poses at Frame {frame_number}')
    ax2.scatter(z_vals, x_vals, y_vals, c='green', s=3)

    for conn in connections:
        ax2.plot([z_vals[conn[0]], z_vals[conn[1]]], 
                  [x_vals[conn[0]], x_vals[conn[1]]], 
                  [y_vals[conn[0]], y_vals[conn[1]]], 'r-')

    ax2.set_xlim(1, -1)
    ax2.set_ylim(0, 1920) 
    ax2.set_zlim(1080, 0)
    ax2.set_xlabel('Z') 
    ax2.set_ylabel('X') 
    ax2.set_zlabel('Y')  
    ax2.grid(True)
   
    plt.savefig(f'{output_dir}/frame_{frame_number}.png')
    plt.close()

# ฟังก์ชันที่ใช้สำหรับ ProcessPoolExecutor
def process_single_frame(frame, total_frames):
    img_path = os.path.join(output_dir, f'frame_{frame}.png')
    if os.path.exists(img_path):
        print(f"ข้ามเฟรมที่: {frame} (ไฟล์มีอยู่แล้ว)")
        return  # ข้ามการสร้างภาพถ้ามีอยู่แล้ว
    
    frame_data = df.loc[df['frames'] == frame].squeeze()
    if not frame_data.empty:  # ตรวจสอบว่าเฟรมไม่ว่าง
        plot_skeleton(frame_data, frame, total_frames)

if __name__ == '__main__':
    selected_frames = df['frames'].tolist()
    total_frames = len(selected_frames)

    # ใช้ ProcessPoolExecutor เพื่อประมวลผลเฟรมแบบขนาน
    with ProcessPoolExecutor(max_workers=6) as executor:
        list(tqdm(executor.map(process_single_frame, selected_frames, [total_frames]*total_frames), total=total_frames))

    print("บันทึกภาพเสร็จสิ้น")
    
    video_path = f'motion-detection/output_video/{file_name}.mp4'
    os.makedirs(video_path, exist_ok=True)
    frame_rate = 60  # กำหนด frame rate ของวิดีโอ
    frame_size = (1920, 1080)  # ขนาดเฟรม (กว้าง x สูง)

    # ใช้ OpenCV ในการสร้างวิดีโอ
    out = cv2.VideoWriter(video_path, cv2.VideoWriter_fourcc(*'mp4v'), frame_rate, frame_size)
    
    # อ่านภาพที่บันทึกไว้และใส่ลงในวิดีโอ
    for idx, frame in enumerate(tqdm(selected_frames)):
        img_path = os.path.join(output_dir, f'frame_{frame}.png')
        
        # ตรวจสอบว่าไฟล์ภาพมีอยู่
        if not os.path.exists(img_path):
            print(f"Warning: ไม่สามารถอ่านไฟล์ {img_path}. ข้ามไป.")
            continue  # ข้ามภาพที่ไม่สามารถอ่านได้
        
        img = cv2.imread(img_path)
        
        if img is None:
            print(f"Error: ไม่สามารถอ่านไฟล์ {img_path}. ข้ามไป.")
            continue  # ข้ามภาพที่ไม่สามารถอ่านได้
        
        # ปรับขนาดภาพ
        img = cv2.resize(img, frame_size)
        
        # เขียนภาพลงในวิดีโอ
        out.write(img)
        
    # ปิดการเขียนวิดีโอ
    out.release()

    print(f'บันทึกวิดีโอ {video_path}')
