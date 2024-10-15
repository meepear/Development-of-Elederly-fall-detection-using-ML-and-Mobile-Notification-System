import pandas as pd
import cv2
import os
import mediapipe as mp
import time
from tqdm import tqdm  # นำเข้า tqdm

# ตั้งค่า MediaPipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# ฟังก์ชันเพื่อสร้าง DataFrame และบันทึกข้อมูลเป็น CSV
def create_csv_from_videos(video_folder, output_folder):
    # ตั้งค่าคอลัมน์ตามที่คุณระบุ
    columns = ["Frames", 'Image_Timestamp', 'Pose_Timestamp'] + \
              ["x0", "y0", "z0",
               "x1", "y1", "z1",
               "x2", "y2", "z2",
               "x3", "y3", "z3",
               "x4", "y4", "z4",
               "x5", "y5", "z5",
               "x6", "y6", "z6",
               "x7", "y7", "z7",
               "x8", "y8", "z8",
               "x9", "y9", "z9",
               "x10", "y10", "z10",
               "x11", "y11", "z11",
               "x12", "y12", "z12",
               "x13", "y13", "z13",
               "x14", "y14", "z14",
               "x15", "y15", "z15",
               "x16", "y16", "z16",
               "x17", "y17", "z17",
               "x18", "y18", "z18",
               "x19", "y19", "z19",
               "x20", "y20", "z20",
               "x21", "y21", "z21",
               "x22", "y22", "z22",
               "x23", "y23", "z23",
               "x24", "y24", "z24",
               "x25", "y25", "z25",
               "x26", "y26", "z26",
               "x27", "y27", "z27",
               "x28", "y28", "z28",
               "x29", "y29", "z29",
               "x30", "y30", "z30",
               "x31", "y31", "z31",
               "x32", "y32", "z32"]

    # สร้าง DataFrame ที่ว่าง
    df = pd.DataFrame(columns=columns)

    # อ่านไฟล์วีดีโอจากโฟลเดอร์ที่ระบุ
    video_files = [f for f in os.listdir(video_folder) if f.endswith(('.mp4', '.avi', '.mov', '.mkv'))]
    
    # ใช้ tqdm ในการแสดง Progress Bar สำหรับไฟล์วีดีโอ
    for video_file in tqdm(video_files, desc="Processing Videos", unit="video"):
        video_path = os.path.join(video_folder, video_file)
        cap = cv2.VideoCapture(video_path)
        frame_count = 0
        start_time = time.time()  # เริ่มจับเวลา

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # เปลี่ยนสีจาก BGR เป็น RGB
            rgb_image_display = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            ih, iw, _ = rgb_image_display.shape  # รับขนาดของภาพจากเฟรมปัจจุบัน
            
            # บันทึก timestamp เมื่อได้รับเฟรม
            image_timestamp = time.time() - start_time
            
            # ประมวลผลภาพด้วย MediaPipe Pose
            results = pose.process(rgb_image_display)

            # บันทึก timestamp เมื่อได้ค่า (x, y, z)
            pose_timestamp = time.time() - start_time
            
            # เตรียมข้อมูลเฟรม
            frame_data = [int(frame_count), image_timestamp, pose_timestamp]  # เปลี่ยน frame_count เป็น int

            # เช็คว่ามี landmark ที่ตรวจจับได้
            if results.pose_landmarks:
                for i, landmark in enumerate(results.pose_landmarks.landmark):
                    x = int(landmark.x * iw)  # ปรับค่า x ให้อยู่ในช่วงพิกเซลของภาพ
                    y = int(landmark.y * ih)  # ปรับค่า y ให้อยู่ในช่วงพิกเซลของภาพ
                    z = landmark.z  # รับค่า Z ของ Landmark
                    frame_data.extend([x, y, z])  # เพิ่ม x, y, z ลงใน frame_data
            
            # ตรวจสอบให้แน่ใจว่าข้อมูลเฟรมมีจำนวนคอลัมน์ตรงตามที่ต้องการ
            if len(frame_data) == len(columns):
                df.loc[len(df)] = frame_data  # เพิ่มแถวใหม่ใน DataFrame
            
            frame_count += 1
            
        cap.release()  # ปิด VideoCapture

        # สร้างชื่อไฟล์ CSV จากชื่อไฟล์วีดีโอ
        csv_filename = os.path.splitext(video_file)[0] + ".csv"  # เปลี่ยนชื่อไฟล์เป็น .csv
        csv_path = os.path.join(output_folder, csv_filename)  # ตั้งที่อยู่ไฟล์ CSV
        df.to_csv(csv_path, index=False)  # บันทึก DataFrame เป็น CSV

# เรียกใช้ฟังก์ชันโดยตรง
video_folder = "vdo"  # โฟลเดอร์ที่เก็บไฟล์วีดีโอ
output_folder = "csv"  # โฟลเดอร์ที่ต้องการบันทึกไฟล์ CSV

os.makedirs(output_folder, exist_ok=True)  # สร้างโฟลเดอร์ csv หากยังไม่มี
create_csv_from_videos(video_folder, output_folder)
print("สร้างไฟล์ CSV เรียบร้อยแล้วในโฟลเดอร์:", output_folder)
