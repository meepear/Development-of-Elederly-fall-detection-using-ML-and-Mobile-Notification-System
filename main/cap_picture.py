import cv2
import os

# ชื่อไฟล์วีดีโอและโฟลเดอร์ที่ต้องการบันทึกรูป
video_file = 'vdo/pun_walk_back_1.mp4'
output_folder = 'picture'

# สร้างโฟลเดอร์ picture ถ้ายังไม่มี
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# สร้างชื่อโฟลเดอร์ย่อยตามชื่อวีดีโอ
video_name = os.path.splitext(os.path.basename(video_file))[0]
video_output_folder = os.path.join(output_folder, f'picture_{video_name}')

# สร้างโฟลเดอร์ย่อยถ้ายังไม่มี
if not os.path.exists(video_output_folder):
    os.makedirs(video_output_folder)

# เปิดวีดีโอ
cap = cv2.VideoCapture(video_file)
frame_count = 0

# ตรวจสอบว่าสามารถเปิดวีดีโอได้หรือไม่
if not cap.isOpened():
    print("Error: Cannot open video.")
else:
    while True:
        ret, frame = cap.read()
        if not ret:  # ถ้าไม่มีเฟรมอีกแล้ว
            break

        # สร้างชื่อไฟล์รูปภาพ
        frame_filename = os.path.join(video_output_folder, f'frame_{frame_count:04d}.jpg')
        
        # บันทึกรูปภาพ
        cv2.imwrite(frame_filename, frame)
        frame_count += 1

    print(f"Saved {frame_count} frames to {video_output_folder}")

# ปิดวีดีโอ
cap.release()
