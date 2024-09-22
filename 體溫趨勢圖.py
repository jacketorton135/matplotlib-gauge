import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
import pymysql
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import datetime

def fetch_body_temperature_status():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='oneokrock12345', database='heart rate monitor')
    cursor = conn.cursor()
    
    try:
        # 查询 '體溫_正常_異常' 列的数据和时间戳
        sql_query = "SELECT `體溫_正常_異常`, `時間戳記` FROM `dht11` ORDER BY `時間戳記` ASC"
        print(f"Executing SQL Query: {sql_query}")
        cursor.execute(sql_query)
        result = cursor.fetchall()
        print(f"Query Result: {result}")
        
        # 将查询结果转换为列表，忽略 `體溫_正常_異常` 为 `None` 的行
        status_list = [(int.from_bytes(row[0], 'big'), row[1]) for row in result if row[0] is not None]
        return status_list
    except pymysql.Error as e:
        print(f"Database error: {e}")
        return []
    finally:
        cursor.close()
        conn.close()

def plot_body_temperature_status(ax, temperature_status):
    if not temperature_status:
        return

    times = [row[1] for row in temperature_status]
    statuses = [row[0] for row in temperature_status]

    # 添加一個額外的時間戳記到 times 列表中
    if len(times) > 0:
        extra_time = times[-1] + datetime.timedelta(seconds=1)
        times.append(extra_time)

    ax.clear()
    ax.stairs(statuses, times, linewidth=2.5)

    ax.set_ylim(-0.1, 1.1)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Normal', 'Error'], fontsize=8)

    # 设置x轴格式化
    ax.xaxis.set_major_locator(mdates.AutoDateLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M:%S'))

    # 调整 x 轴标签字体大小
    plt.setp(ax.get_xticklabels(), rotation=45, ha='right', fontsize=6)

    ax.set_xlabel('Time')
    ax.set_ylabel('Body Temperature Status')
    ax.set_title('Body Temperature Status Over Time')

def update_plot():
    temperature_status = fetch_body_temperature_status()
    plot_body_temperature_status(ax, temperature_status)
    canvas.draw()
    root.after(5000, update_plot)  # 每5秒更新一次

# 创建Tkinter窗口
root = tk.Tk()
root.title("Real-time Body Temperature 趨勢圖")

fig, ax = plt.subplots(figsize=(10, 6))  # 調整畫布大小
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)

update_plot()  # 初始调用更新函数

root.mainloop()



