import cv2
import mediapipe as mp
import os
from tqdm import tqdm  # นำเข้า tqdm สำหรับ progress bar

# กำหนดเส้นทางโฟลเดอร์
input_folder = 'vdo'
output_folder = 'vdo_pose'

# สร้างโฟลเดอร์ output ถ้ายังไม่มี
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# กำหนด Mediapipe Pose
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5)

# ฟังก์ชันสำหรับประมวลผลวิดีโอ
def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # ใช้ tqdm เพื่อสร้าง progress bar
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    with tqdm(total=total_frames, desc="Processing Video", unit="frame") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            
            # แปลงภาพจาก BGR เป็น RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(frame_rgb)

            # วาดจุด pose ตามที่กำหนด
            if results.pose_landmarks:
                iw, ih = frame.shape[1], frame.shape[0]
                connections = [
                    (11, 12), (12, 24), (24, 23), (23, 11),
                    (15, 13), (13, 11), (12, 14), (14, 16),
                    (23, 25), (25, 27), (24, 26), (26, 28)
                ]

                # วาดเส้นเชื่อมต่อ
                for connection in connections:
                    pt1 = results.pose_landmarks.landmark[connection[0]]
                    pt2 = results.pose_landmarks.landmark[connection[1]]
                    x1, y1 = int(pt1.x * iw), int(pt1.y * ih)
                    x2, y2 = int(pt2.x * iw), int(pt2.y * ih)
                    cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                # คำนวณ Center of Gravity ระหว่างจุดที่ 24 และ 23
                pt_24 = results.pose_landmarks.landmark[24]
                pt_23 = results.pose_landmarks.landmark[23]
                cog_x = int((pt_24.x + pt_23.x) / 2 * iw)
                cog_y = int((pt_24.y + pt_23.y) / 2 * ih)

                # วาดจุด Center of Gravity
                cv2.circle(frame, (cog_x, cog_y), 5, (255, 0, 0), -1)  # จุดสีฟ้า

                # เชื่อม Center of Gravity กับ landmark 0
                pt_0 = results.pose_landmarks.landmark[0]
                x0, y0 = int(pt_0.x * iw), int(pt_0.y * ih)
                cv2.line(frame, (cog_x, cog_y), (x0, y0), (255, 0, 0), 2)
            
            out.write(frame)

            # อัปเดต progress bar
            pbar.update(1)

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# ประมวลผลวิดีโอทั้งหมดในโฟลเดอร์
for filename in os.listdir(input_folder):
    if filename.endswith('.mp4'):  # รองรับเฉพาะไฟล์ mp4
        input_file_path = os.path.join(input_folder, filename)
        output_file_path = os.path.join(output_folder, f'pose_{filename}')
        process_video(input_file_path, output_file_path)
        print(f'Processed {filename} and saved as {output_file_path}')
