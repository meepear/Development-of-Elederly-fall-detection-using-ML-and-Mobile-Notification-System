import os
import cv2
import mediapipe as mp
import csv
from tqdm import tqdm
from PyQt6.QtWidgets import QApplication, QFileDialog, QWidget

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose

def process_video_to_csv(video_path, output_csv_folder):
    # Get video name without extension
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    
    # Path for the CSV file
    csv_file = os.path.join(output_csv_folder, f"{video_name}.csv")
    
    # Check if CSV already exists, skip if it does
    if os.path.exists(csv_file):
        print(f"File {csv_file} already exists. Skipping...")
        return
    
    cap = cv2.VideoCapture(video_path)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    # Data to store landmarks
    data = []
    
    # Process each frame
    with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
        for frame_counter in tqdm(range(total_frames), desc=f"Processing {video_name}", ncols=100, colour='blue'):
            success, image = cap.read()
            if not success:
                break
            
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = pose.process(image_rgb)
            
            if results.pose_landmarks:
                frame_landmarks = [frame_counter]
                ih, iw, _ = image.shape
                
                for landmark in results.pose_landmarks.landmark:
                    x = int(landmark.x * iw)
                    y = int(landmark.y * ih)
                    z = landmark.z
                    frame_landmarks.extend([x, y, z])
                
                data.append(frame_landmarks)
    
    cap.release()
    
    # Write data to CSV
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Writing headers
        headers = ["frames"] + [f"x{i}, y{i}, z{i}" for i in range(33)]
        writer.writerow(headers)
        writer.writerows(data)
    
    print(f"Finished writing {csv_file}")

def select_folder_and_process():
    app = QApplication([])  # เริ่มการทำงานของ PyQt6
    folder_dialog = QFileDialog()  # สร้างหน้าต่างการเลือกไฟล์
    folder_dialog.setFileMode(QFileDialog.FileMode.Directory)  # กำหนดให้เลือกเฉพาะโฟลเดอร์
    
    if folder_dialog.exec():  # ถ้าเลือกโฟลเดอร์แล้ว
        folder_path = folder_dialog.selectedFiles()[0]  # รับเส้นทางโฟลเดอร์ที่เลือก
        
        # Create a folder for CSV files if not exists
        output_csv_folder = os.path.join(folder_path, "csv_folder")
        if not os.path.exists(output_csv_folder):
            os.makedirs(output_csv_folder)
        
        # Get all video files in the folder
        video_extensions = ['.mp4', '.avi', '.mov', '.mkv']
        video_files = [f for f in os.listdir(folder_path) if os.path.splitext(f)[1] in video_extensions]
        
        for video_file in video_files:
            video_path = os.path.join(folder_path, video_file)
            process_video_to_csv(video_path, output_csv_folder)
    
    app.quit()  # ปิดแอปพลิเคชันเมื่อเสร็จสิ้น

if __name__ == "__main__":
    select_folder_and_process()
