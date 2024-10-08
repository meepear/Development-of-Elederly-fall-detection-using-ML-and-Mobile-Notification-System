# ไลบรารีสำหรับการประมวลผลภาพและวิดีโอ
import cv2 
# ไลบรารีสำหรับการวิเคราะห์ภาพและตรวจจับท่าทาง รวมถึงการทำงานกับ Landmark ของร่างกาย
import mediapipe as mp
# ไลบรารีสำหรับการอ่านและเขียนไฟล์ CSV
import csv  
from tqdm import tqdm  # ใช้สำหรับ Progress Bar
import os


# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

# นำเข้า Video
video_name = 'Nam'
video_path = f"Video/{video_name}.mp4"  # กำหนด Path
cap = cv2.VideoCapture(video_path)  # เปิดไฟล์วิดีโอ
# cap = cv2.VideoCapture()

# สร้างโฟลเดอร์สำหรับเก็บภาพแต่ละเฟรม
output_folder = f"images/frames_{video_name}"
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ใช้สำหรับนับเฟรม
frame_counter = 0  # ตัวแปรนับจำนวนเฟรม
# อาร์เรย์ข้อมูล
data = []  # อาร์เรย์สำหรับเก็บข้อมูลตำแหน่งของ Landmark

# ตรวจสอบจำนวนเฟรมทั้งหมดในวิดีโอ
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # จำนวนเฟรมทั้งหมดในวิดีโอ

# กำหนดค่าในการตรวจจับ (min_detection_confidence) และการติดตาม (min_tracking_confidence)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    # ใช้ tqdm เพื่อแสดง Progress Bar ในขณะที่วนลูปเฟรมทั้งหมด
    for frame_counter in tqdm(range(total_frames), desc="Processing frames", ncols=100, colour='blue'):
        success, image = cap.read()  # อ่านเฟรมถัดไปจากวิดีโอ
        if not success:  # ถ้าไม่สามารถอ่านเฟรมได้
            break

        # บันทึกภาพเป็นไฟล์ในรูปแบบ PNG โดยตั้งชื่อไฟล์ตามลำดับเฟรม
        image_filename = f"{output_folder}/image_frame_{frame_counter}.png"
        cv2.imwrite(image_filename, image)

        # แปลงภาพจาก BGR เป็น RGB เพื่อให้ใช้งานกับ MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # จับ Landmark ทั้งหมดในภาพ
        results = pose.process(image_rgb)

        if results.pose_landmarks:  # ถ้าตรวจจับ Landmark ได้
            # เตรียมลิสต์เพื่อเก็บตำแหน่ง Landmark ของเฟรมนี้
            frame_landmarks = [frame_counter]
            
            for id, landmark in enumerate(results.pose_landmarks.landmark):  # วนลูปผ่าน Landmark แต่ละจุด
                ih, iw, _ = image.shape  # รับขนาดของภาพ (ความสูง, ความกว้าง)
                x = int(landmark.x * iw)  # ปรับค่า x ให้อยู่ในช่วงพิกเซลของภาพ
                y = int(landmark.y * ih)  # ปรับค่า y ให้อยู่ในช่วงพิกเซลของภาพ
                z = landmark.z  # รับค่า Z ของ Landmark

                # เพิ่ม x, y, z ลงในลิสต์ frame_landmarks
                frame_landmarks.append(x)  # เพิ่มค่า x
                frame_landmarks.append(y)  # เพิ่มค่า y
                frame_landmarks.append(z)  # เพิ่มค่า z

            # เพิ่มตำแหน่ง Landmark ของเฟรมนี้ลงในอาร์เรย์ data
            data.append(frame_landmarks)  # เก็บข้อมูล Landmark ของเฟรมนี้ใน data
            
# ปล่อยวิดีโอเมื่ออ่านเสร็จสิ้น
cap.release()


# *******************************************เพิ่ม elapsed time ในคอลัม 5/10/2024
# รวมโค้ดส่วนของ csv เข้าไปทำงานในขั้นตอน pose แล้วเพิ่มคอลั่ม
# 1. เวลาที่อ้างอิงจาก elapsed time หลังจากที่ได้ ภาพ 
# 2. เวลาที่อ้างอิงจาก elapsed time หลังจากที่ได้ Pose
# เขียนข้อมูลลงในไฟล์ CSV
with open(f'motion-detection/{video_name}.csv', mode='w', newline='') as file:
    writer = csv.writer(file)  # สร้างวัตถุ writer สำหรับเขียนข้อมูลในรูปแบบ CSV
    writer.writerow(["frames",  # เขียนชื่อคอลัมน์ในไฟล์ CSV
                     "x0", "y0", "z0",
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
                     "x32", "y32", "z32"])
    writer.writerows(data)  # เขียนข้อมูล Landmark ทั้งหมดลงในไฟล์ CSV
    
print("เสร็จสิ้นการเขียนข้อมูลในไฟล์ .csv")  # แจ้งผลลัพธ์เมื่อเขียนข้อมูลเสร็จสิ้น
