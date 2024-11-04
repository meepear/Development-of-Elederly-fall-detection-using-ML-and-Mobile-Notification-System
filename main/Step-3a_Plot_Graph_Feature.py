import pandas as pd
import matplotlib.pyplot as plt

# ฟังก์ชันสำหรับสร้างกราฟ
def plot_graphs():
    # อ่านข้อมูลจากไฟล์ CSV
    data_name = input('Data File CSV name: ')
    data_path = f'csv/{data_name}.csv'
    data = pd.read_csv(data_path)

    # กรองข้อมูลเพื่อข้ามค่าที่เป็นศูนย์
    data_filtered = data[(data['Movement_Rate'] != 0) & (data['CoG_Angles'] != 0)]

    print(data_filtered[['Movement_Rate', 'CoG_Angles']].describe())
    
    plt.figure(figsize=(12, 6))
    
    # สร้างกราฟ Movement Rate
    plt.subplot(1, 3, 1)
    plt.plot(data_filtered.index, data_filtered['Movement_Rate'], color='blue', linestyle='-', linewidth=1) 
    plt.title('Movement Rate')
    plt.xlabel('Frame')
    plt.ylabel('Movement Rate')

    # สร้างกราฟ Center of Gravity Angles
    plt.subplot(1, 3, 2)
    plt.plot(data_filtered.index, data_filtered['CoG_Angles'], color='red', linestyle='-', linewidth=1) 
    plt.title('Center of Gravity Angles')
    plt.xlabel('Frame')
    plt.ylabel('Center of Gravity Angles')
    
    # สร้างกราฟ Scatter Plot ของ Movement Rate และ Center of Gravity Angles
    plt.subplot(1, 3, 3)
    plt.scatter(data_filtered['Movement_Rate'], data_filtered['CoG_Angles'], color='purple', alpha=0.5)
    plt.title('Movement Rate vs Center of Gravity Angles')
    plt.xlabel('Movement Rate')
    plt.ylabel('Center of Gravity Angles')

    # แสดงกราฟ
    plt.tight_layout()
    plt.show()

# เรียกใช้งานฟังก์ชัน
plot_graphs()
