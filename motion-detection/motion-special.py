import cv2
import mediapipe as mp
import csv
import time
import os  # ไลบรารีสำหรับจัดการกับไฟล์และโฟลเดอร์
from tqdm import tqdm

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

# ตั้งค่าโฟลเดอร์ที่เก็บภาพ
image_folder = 'pictures'  # โฟลเดอร์ที่มีรูปภาพ
output_folder = 'output_images'  # โฟลเดอร์สำหรับเก็บไฟล์ภาพที่ประมวลผลแล้ว

# ตรวจสอบว่ามีโฟลเดอร์สำหรับเก็บภาพหรือไม่ ถ้าไม่มีให้สร้างขึ้นมา
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# ใช้สำหรับนับภาพ
image_counter = 0
# อาร์เรย์ข้อมูล
data = []

# รับรายชื่อไฟล์ภาพทั้งหมดในโฟลเดอร์ที่กำหนด
image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
total_images = len(image_files)

# กำหนดค่าในการตรวจจับ (min_detection_confidence) และการติดตาม (min_tracking_confidence)
with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    for image_file in tqdm(image_files, desc="Processing images", ncols=100, colour='blue'):
        start_time = time.time()  # เริ่มจับเวลาเมื่ออ่านภาพ

        # อ่านภาพจากไฟล์
        image_path = os.path.join(image_folder, image_file)
        image = cv2.imread(image_path)

        if image is None:
            print(f"ไม่สามารถเปิดภาพ {image_file} ได้")
            continue

        # บันทึกภาพต้นฉบับในโฟลเดอร์
        image_filename = f"{output_folder}/image_frame_{image_counter}.png"
        cv2.imwrite(image_filename, image)

        # แปลงภาพจาก BGR เป็น RGB เพื่อใช้กับ MediaPipe
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # จับ Landmark ทั้งหมดในภาพ
        results = pose.process(image_rgb)

        image_process_time = time.time()  # จับเวลาหลังจากที่ได้ภาพ

        if results.pose_landmarks:
            frame_landmarks = [image_counter]  # เก็บลำดับของภาพ

            for id, landmark in enumerate(results.pose_landmarks.landmark):
                ih, iw, _ = image.shape
                x = int(landmark.x * iw)
                y = int(landmark.y * ih)
                z = landmark.z

                frame_landmarks.extend([x, y, z])

            # เพิ่มเวลาที่จับได้หลังจากที่ได้ Pose ลงในข้อมูล
            pose_process_time = time.time()  # จับเวลาหลังจากที่ได้ Pose
            elapsed_image_time = image_process_time - start_time  # เวลาจากการได้ภาพ
            elapsed_pose_time = pose_process_time - image_process_time  # เวลาจากการได้ Pose
            frame_landmarks.append(elapsed_image_time)  # เพิ่มเวลาหลังจากได้ภาพ
            frame_landmarks.append(elapsed_pose_time)   # เพิ่มเวลาหลังจากได้ Pose

            # เพิ่มข้อมูลใน data
            data.append(frame_landmarks)

        image_counter += 1  # เพิ่มลำดับภาพ

# เขียนข้อมูลลงในไฟล์ CSV
with open(f'motion-detection/images_landmarks.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    # เพิ่มคอลัมน์สำหรับเวลาหลังจากได้ภาพและ Pose
    writer.writerow(["image_index",
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
                     "x32", "y32", "z32",
                     "elapsed_image_time", "elapsed_pose_time"])
    writer.writerows(data)

print("เสร็จสิ้นการเขียนข้อมูลในไฟล์ .csv และบันทึกภาพทั้งหมด")
