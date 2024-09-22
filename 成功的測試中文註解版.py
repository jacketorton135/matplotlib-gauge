import tkinter as tk  # 匯入 tkinter 模組，用於創建圖形用戶界面
from tkinter import ttk  # 匯入 tkinter 的 ttk 模組，用於創建改進的 GUI 元件
from datetime import datetime  # 匯入 datetime 模組，用於處理日期和時間
import pymysql  # 匯入 pymysql 模組，用於操作 MySQL 資料庫
import io  # 匯入 io 模組，用於處理 I/O 操作
from PIL import Image, ImageTk, ImageOps, ImageDraw  # 匯入 PIL 模組，用於圖像處理
import matplotlib.pyplot as plt  # 匯入 matplotlib 的 pyplot 模組，用於創建圖表
import numpy as np  # 匯入 numpy 模組，用於數據處理
import webbrowser  # 匯入 webbrowser 模組，用於開啟網頁
import requests  # 匯入 requests 模組，用於發送 HTTP 請求
import csv  # 匯入 csv 模組，用於處理 CSV 文件
from apscheduler.schedulers.background import BackgroundScheduler  # 匯入 apscheduler 模組，用於定時任務調度
import time  # 匯入 time 模組，用於時間處理
import os  # 匯入 os 模組，用於操作系統功能
import matplotlib.dates as mdates  # 匯入 matplotlib.dates 模組，用於處理日期格式
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # 匯入 matplotlib 的 tkinter 背後繪圖畫布模組
from matplotlib.patches import Wedge  # 匯入 matplotlib 的 Wedge 類別，用於繪製圓形扇形
from matplotlib.animation import FuncAnimation  # 匯入 matplotlib 的 FuncAnimation 類別，用於創建動畫
from data_sync import connect_and_sync  # 從 data_sync 模組匯入 connect_and_sync 函數

def start_data_sync():
    connect_and_sync()  # 呼叫 connect_and_sync 函數進行數據同步
    button = tk.Button(button_frame, text="連線", command=connect_and_sync)  # 創建一個按鈕，點擊時進行數據同步
    print("數據同步已啟動")  # 在控制台打印數據同步啟動的消息

def generate_qr_code(data, filename="linebotchat.png"):
    qr = qrcode.QRCode(
        version=1,  # 設定 QR 碼的版本
        error_correction=qrcode.constants.ERROR_CORRECT_L,  # 設定錯誤糾正級別
        box_size=5,  # 設定每個框的像素大小
        border=4,  # 設定邊框的框數
    )
    qr.add_data(data)  # 添加數據到 QR 碼中
    qr.make(fit=True)  # 使 QR 碼適應數據大小
    img = qr.make_image(fill_color="black", back_color="white")  # 生成 QR 碼圖像，設置前景色和背景色
    img.save(filename)  # 將 QR 碼圖像保存到指定文件

def open_qr_code():
    filename = "F:\\物聯網123\\視覺化\\linebotchat.png"  # 指定 QR 碼圖像的文件名
    if not os.path.exists(filename):  # 如果文件不存在
        generate_qr_code("https://example.com", filename)  # 生成 QR 碼圖像
    os.startfile(filename)  # 在 Windows 系統中打開文件



# GUI 函數
def create_gauge_image(current_value, min_value=0, max_value=50):
    fig, ax = plt.subplots(figsize=(2.5, 2), subplot_kw={'projection': 'polar'})  # 創建極坐標系的圖形和軸
    current_value = max(min_value, min(current_value, max_value))  # 限制當前值在最小值和最大值之間
    ax.set_thetamin(0)  # 設定極坐標的最小角度
    ax.set_thetamax(180)  # 設定極坐標的最大角度
    ax.set_ylim(0, 1)  # 設定極坐標的半徑範圍
    ax.set_yticks([])  # 隱藏 y 軸刻度
    ax.set_xticks([])  # 隱藏 x 軸刻度
    colors = ["#2bad4e", "#eff229", "#f25829"]  # 定義顏色列表
    colors_text = ["LOW", "Normal", "HIGH"]  # 定義顏色對應的文字
    bounds = np.linspace(0, np.pi, len(colors) + 1)  # 計算顏色區間的角度範圍
    for i in range(len(colors)):  # 遍歷每種顏色
        ax.fill_between(np.linspace(bounds[i], bounds[i+1], 100), 0.6, 1, color=colors[i], alpha=0.3)  # 填充顏色區域
        mid_angle = (bounds[i] + bounds[i+1]) / 2  # 計算顏色區域的中間角度
        ax.text(mid_angle, 0.8, colors_text[i], ha='center', va='center', fontsize=10, color='black')  # 在顏色區域中間添加文字
    value_angle = np.interp(current_value, [min_value, max_value], [0, np.pi])  # 計算當前值對應的角度
    ax.plot([value_angle, value_angle], [0, 0.5], color='black', linewidth=2)  # 繪製指針
    ax.text(0, -0.2, f"IoT sensor Level\nValue = {current_value:.2f}", ha='center', va='center')  # 添加當前值的文字說明
    buf = io.BytesIO()  # 創建內存中的緩衝區
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches=0)  # 保存圖形到緩衝區
    buf.seek(0)  # 重置緩衝區的位置
    plt.close(fig)  # 關閉圖形
    return Image.open(buf)  # 返回圖像對象

def create_circle_image(color, radius=20):
    fig, ax = plt.subplots(figsize=(2*radius/100, 2*radius/100), dpi=100)  # 創建一個圖形和軸，設置大小和解析度
    ax.add_patch(plt.Circle((0.5, 0.5), 0.5, color=color))  # 添加圓形補丁到圖形中
    ax.set_xlim(0, 1)  # 設定 x 軸的範圍
    ax.set_ylim(0, 1)  # 設定 y 軸的範圍
    ax.axis('off')  # 隱藏坐標軸
    buf = io.BytesIO()  # 創建內存中的緩衝區
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight', pad_inches=0)  # 保存圖形到緩衝區
    buf.seek(0)  # 重置緩衝區的位置
    plt.close(fig)  # 關閉圖形
    image = Image.open(buf)  # 打開圖像對象
    image = ImageOps.fit(image, (radius*2, radius*2), centering=(0.5, 0.5))  # 裁剪圖像為圓形
    mask = Image.new('L', (radius*2, radius*2), 0)  # 創建一個新的黑色蒙版圖像
    draw = ImageDraw.Draw(mask)  # 創建繪圖對象
    draw.ellipse((0, 0, radius*2, radius*2), fill=255)  # 在蒙版上繪製白色圓形
    image.putalpha(mask)  # 將蒙版應用到圖像上
    return image  # 返回圖像對象

def show_current_time():
    current_time = datetime.now().strftime("系統時間:%Y-%m-%d %H:%M:%S")  # 獲取當前時間並格式化
    time_label.config(text=current_time)  # 更新時間標籤的文本
    main_window.after(1000, show_current_time)  # 每秒調用一次 show_current_time 函數

def toggle_treeview():
    if treeview_frame.winfo_viewable():  # 如果 treeview_frame 可見
        treeview_frame.pack_forget()  # 隱藏 treeview_frame
    else:
        treeview_frame.pack(fill=tk.BOTH, expand=True)  # 顯示 treeview_frame，並擴展以填充父容器
        load_data_from_db()  # 從資料庫加載數據

def load_data_from_db():
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='oneokrock12345', database='heart rate monitor')  # 連接到 MySQL 資料庫
    cursor = conn.cursor()  # 創建資料庫游標

    for item in tree.get_children():  # 遍歷 tree 的所有子項
        tree.delete(item)  # 刪除每個子項

    tables = ['heart_rate', 'dht11', 'bmi']  # 定義要查詢的表名
    table_structures = {}  # 創建空字典存儲表結構
    for table in tables:  # 遍歷每個表
        cursor.execute(f"DESCRIBE {table}")  # 查詢表的結構
        table_structures[table] = [row[0] for row in cursor.fetchall()]  # 存儲表的列名

    print("Table structures:", table_structures)  # 打印表結構

    time_column = {table: '時間戳記' for table in tables}  # 定義時間戳記列的名稱
    print("Time columns:", time_column)  # 打印時間戳記列名稱

    query = f"""
    SELECT * FROM (
        SELECT 
            COALESCE(hr.{time_column['heart_rate']}, d.{time_column['dht11']}, b.{time_column['bmi']}) as timestamp,
            hr.心跳 as heart_rate, hr.心跳狀態 as heart_rate_status,
            d.溫度 as temperature, d.濕度 as humidity, d.體溫 as body_temperature, 
            d.溫度狀態 as temperature_status, d.濕度狀態 as humidity_status, d.體溫狀態 as body_temperature_status,
            b.BMI as bmi, b.檢查結果 as bmi_status
        FROM 
            heart_rate hr
        LEFT JOIN 
            dht11 d ON hr.{time_column['heart_rate']} = d.{time_column['dht11']}
        LEFT JOIN 
            bmi b ON hr.{time_column['heart_rate']} = b.{time_column['bmi']}
        WHERE 
            hr.心跳狀態 != '心跳正常'
            OR d.溫度狀態 != '溫度正常'
            OR d.濕度狀態 != '濕度正常'
            OR d.體溫狀態 != '體溫正常'
            OR b.檢查結果 IN ('體重過輕', '過重', '輕度肥胖', '重度肥胖')
        UNION
        SELECT 
            COALESCE(hr.{time_column['heart_rate']}, d.{time_column['dht11']}, b.{time_column['bmi']}) as timestamp,
            hr.心跳 as heart_rate, hr.心跳狀態 as heart_rate_status,
            d.溫度 as temperature, d.濕度 as humidity, d.體溫 as body_temperature, 
            d.溫度狀態 as temperature_status, d.濕度狀態 as humidity_status, d.體溫狀態 as body_temperature_status,
            b.BMI as bmi, b.檢查結果 as bmi_status
        FROM 
            dht11 d
        LEFT JOIN 
            heart_rate hr ON d.{time_column['dht11']} = hr.{time_column['heart_rate']}
        LEFT JOIN 
            bmi b ON d.{time_column['dht11']} = b.{time_column['bmi']}
        WHERE 
            hr.心跳狀態 != '心跳正常'
            OR d.溫度狀態 != '溫度正常'
            OR d.濕度狀態 != '濕度正常'
            OR d.體溫狀態 != '體溫正常'
            OR b.檢查結果 IN ('體重過輕', '過重', '輕度肥胖', '重度肥胖')
        UNION
        SELECT 
            COALESCE(hr.{time_column['heart_rate']}, d.{time_column['dht11']}, b.{time_column['bmi']}) as timestamp,
            hr.心跳 as heart_rate, hr.心跳狀態 as heart_rate_status,
            d.溫度 as temperature, d.濕度 as humidity, d.體溫 as body_temperature, 
            d.溫度狀態 as temperature_status, d.濕度狀態 as humidity_status, d.體溫狀態 as body_temperature_status,
            b.BMI as bmi, b.檢查結果 as bmi_status
        FROM 
            bmi b
        LEFT JOIN 
            heart_rate hr ON b.{time_column['bmi']} = hr.{time_column['heart_rate']}
        LEFT JOIN 
            dht11 d ON b.{time_column['bmi']} = d.{time_column['dht11']}
        WHERE 
            hr.心跳狀態 != '心跳正常'
            OR d.溫度狀態 != '溫度正常'
            OR d.濕度狀態 != '濕度正常'
            OR d.體溫狀態 != '體溫正常'
            OR b.檢查結果 IN ('體重過輕', '過重', '輕度肥胖', '重度肥胖')
    ) AS combined_data
    ORDER BY timestamp DESC
    """

    print("Generated query:", query)  # 打印生成的 SQL 查詢語句


    try:
        cursor.execute(query)  # 執行查詢語句
        abnormal_data = cursor.fetchall()  # 獲取所有異常數據

        for row in abnormal_data:  # 遍歷每一行異常數據
            timestamp, heart_rate, heart_rate_status, temperature, humidity, body_temp, temperature_status, humidity_status, body_temp_status, bmi, bmi_status = row  # 解包數據行

            abnormal_values = []  # 儲存異常值的列表
            abnormal_statuses = []  # 儲存異常狀態的列表

            if heart_rate_status and heart_rate_status != '心跳正常':  # 如果心跳狀態不正常
                abnormal_values.append(f"{heart_rate}")  # 添加心跳值到異常值列表
                abnormal_statuses.append(heart_rate_status)  # 添加心跳狀態到異常狀態列表
            if temperature_status and temperature_status != '溫度正常':  # 如果溫度狀態不正常
                abnormal_values.append(f"{temperature}")  # 添加溫度值到異常值列表
                abnormal_statuses.append(temperature_status)  # 添加溫度狀態到異常狀態列表
            if humidity_status and humidity_status != '濕度正常':  # 如果濕度狀態不正常
                abnormal_values.append(f"{humidity}")  # 添加濕度值到異常值列表
                abnormal_statuses.append(humidity_status)  # 添加濕度狀態到異常狀態列表
            if body_temp_status and body_temp_status != '體溫正常':  # 如果體溫狀態不正常
                abnormal_values.append(f"{body_temp}")  # 添加體溫值到異常值列表
                abnormal_statuses.append(body_temp_status)  # 添加體溫狀態到異常狀態列表
            if bmi_status in ['體重過輕', '過重', '輕度肥胖', '重度肥胖']:  # 如果 BMI 狀態為異常
                abnormal_values.append(f"{bmi}")  # 添加 BMI 值到異常值列表
                abnormal_statuses.append(bmi_status)  # 添加 BMI 狀態到異常狀態列表

            if abnormal_values and abnormal_statuses:  # 如果有異常值和異常狀態
                tree.insert("", "end", values=(timestamp, ", ".join(abnormal_values), ", ".join(abnormal_statuses)))  # 插入到 treeview 中

    except pymysql.Error as e:  # 捕獲資料庫異常
        print(f"Database error: {e}")  # 打印異常信息
    finally:
        cursor.close()  # 關閉資料庫游標
        conn.close()  # 關閉資料庫連接

def create_gauge(fig, ax, min_value, max_value, ranges):
    arrow = ax.arrow(0.5, 0, 0, 0.3, width=0.02, head_width=0.05, head_length=0.07, fc='black', ec='black')
    colors = ["#2bad4e", "#eff229", "#f25829"]  # 定義顏色列表
    color_texts = ["LOW", "Normal", "HIGH"]  # 定義顏色對應的文字
    angle_ranges = [0, 60, 120]  # 定義顏色區間的角度範圍

    # 增加圖表的尺寸
    fig.set_size_inches(4, 2)  # 調整這裡的數值來增加表頭之間的距離

    for i in range(len(colors)):  # 遍歷每種顏色
        start_angle = angle_ranges[i]  # 獲取顏色區域的起始角度
        end_angle = angle_ranges[i] + 60  # 獲取顏色區域的結束角度
        wedge = Wedge((0.5, 0), 0.4, start_angle, end_angle, width=0.1, facecolor=colors[i])  # 創建扇形區域
        ax.add_artist(wedge)  # 添加扇形區域到圖形中

        mid_angle = np.radians(angle_ranges[i] + 30)  # 計算顏色區域的中間角度
        x = 0.5 + 0.35 * np.cos(mid_angle)  # 計算文字的 x 座標
        y = 0.35 * np.sin(mid_angle)  # 計算文字的 y 座標
        ax.text(x, y, color_texts[i], ha='center', va='center', fontsize=10, color='black')  # 在扇形區域中間添加文字，並設置字體大小

    arrow = ax.arrow(0.5, 0, 0, 0.3, width=0.02, head_width=0.05, head_length=0.07, fc='black', ec='black')  # 創建箭頭

    ax.set_xlim(0, 1)  # 設定 x 軸的範圍
    ax.set_ylim(-0.1, 0.5)  # 設定 y 軸的範圍
    ax.axis('off')  # 隱藏坐標軸

    def set_needle(value):  # 定義設置指針的函數
        nonlocal arrow  # 使用外部作用域的 arrow 變量
        if value <= ranges[0][1]:  # 根據值設定指針角度
            angle = 45
        elif value <= ranges[1][1]:
            angle = 90
        else:
            angle = 135

        rad = np.radians(angle)  # 將角度轉換為弧度
        dx = 0.3 * np.cos(rad)  # 計算指針的 x 方向增量
        dy = 0.3 * np.sin(rad)  # 計算指針的 y 方向增量
        
        arrow.remove()
        arrow = ax.arrow(0.5, 0, dx, dy, width=0.02, head_width=0.05, head_length=0.07, fc='black', ec='black')
        ax.add_artist(arrow)
        return arrow

    return arrow, set_needle  # 返回指針和設置指針的函數

def is_high_or_low(value, ranges):
    # 判斷數值是否在範圍外（高或低）
    return value <= ranges[0][1] or value >= ranges[2][0]

def add_labels_and_buttons(frame, fig, ax, ranges, value, google_sheet_url=None):
    # 在指定的框架中添加標籤和按鈕
    
    label_frame = tk.Frame(frame)  # 創建標籤框架
    label_frame.pack(side="left", padx=5, pady=5)  # 將標籤框架放置在左側，並設置邊距

    label = tk.Label(label_frame, text=value)  # 創建顯示值的標籤
    label.pack()  # 將標籤放置在標籤框架中

    canvas = FigureCanvasTkAgg(fig, master=label_frame)  # 創建圖形的 Canvas
    canvas.draw()  # 繪製 Canvas
    canvas.get_tk_widget().pack()  # 將 Canvas 添加到標籤框架中

    button_frame = tk.Frame(label_frame)  # 創建按鈕框架
    button_frame.pack(fill=tk.X, padx=2, pady=2)  # 將按鈕框架放置在標籤框架中，並設置邊距

    green_circle_image = create_circle_image("green", radius=20)  # 創建綠色圓形圖片
    red_circle_image = create_circle_image("red", radius=20)  # 創建紅色圓形圖片
    green_circle_photo = ImageTk.PhotoImage(green_circle_image)  # 將綠色圓形圖片轉換為 PhotoImage
    red_circle_photo = ImageTk.PhotoImage(red_circle_image)  # 將紅色圓形圖片轉換為 PhotoImage

    green_button = tk.Label(button_frame, image=green_circle_photo, width=40, height=40)  # 創建綠色圓形按鈕
    green_button.image = green_circle_photo  # 保存圖片引用
    green_button.pack(side=tk.LEFT, padx=2)  # 將綠色圓形按鈕放置在按鈕框架中

    red_button = tk.Label(button_frame, image=red_circle_photo, width=40, height=40)  # 創建紅色圓形按鈕
    red_button.image = red_circle_photo  # 保存圖片引用
    red_button.pack_forget()  # 初始時隱藏紅色圓形按鈕
    
    button_frame_bottom = tk.Frame(button_frame)  # 創建按鈕框架底部
    button_frame_bottom.pack(fill=tk.X, pady=5)  # 將底部按鈕框架放置在按鈕框架中

    trend_button = tk.Button(button_frame_bottom, text="趨勢圖", command=lambda: open_trend_chart(value))  # 創建趨勢圖按鈕
    trend_button.pack(side='left', padx=2, pady=2)  # 將趨勢圖按鈕放置在底部按鈕框架中

    if google_sheet_url:
        google_sheet_button = tk.Button(button_frame_bottom, text="Google Sheet連結", command=lambda: webbrowser.open(google_sheet_url))  # 創建 Google Sheet 連結按鈕
        google_sheet_button.pack(side='left', padx=2, pady=2)  # 將 Google Sheet 連結按鈕放置在底部按鈕框架中

    label = tk.Label(label_frame, text="指針圖", font=("Arial", 10))  # 創建指針圖的標籤
    label.pack(padx=2, pady=2)  # 將標籤放置在標籤框架中
    
    return canvas, green_button, red_button  # 返回 Canvas、綠色圓形按鈕和紅色圓形按鈕


def open_trend_chart(value):
    # 根據值打開對應的趨勢圖文件
    chart_files = {
        "溫度": "溫度趨勢圖.py",
        "濕度": "濕度趨勢圖.py",
        "體溫": "體溫趨勢圖.py",
        "心跳": "心跳趨勢圖.py",
        "BMI": "bmi趨勢圖.py"
    }
    
    chart_file = chart_files.get(value)  # 獲取對應的趨勢圖文件
    if chart_file:
        os.system(f'python {chart_file}')  # 執行趨勢圖文件
    else:
        print(f"No trend chart file found for {value}")  # 如果找不到文件，打印錯誤信息

def open_looker_studio():
    # 打開 Looker Studio 的報告頁面
    url = "https://lookerstudio.google.com/reporting/8661248a-16c8-4735-8d06-5aceb1613022/page/pwl4D"
    webbrowser.open(url)  # 在瀏覽器中打開 URL

# GUI 設置
main_window = tk.Tk()  # 創建主窗口
main_window.title("MR蔣監控系統")  # 設置主窗口標題
main_window.geometry("1000x900")  # 設置主窗口大小

main_frame = tk.Frame(main_window)  # 創建主框架
main_frame.pack(fill=tk.BOTH, expand=True)  # 填滿整個窗口並擴展

top_frame = tk.Frame(main_window)  # 創建頂部框架
top_frame.pack(side=tk.TOP, fill=tk.X)  # 將頂部框架放置在窗口的頂部，並填滿 X 軸

bottom_frame = tk.Frame(main_window)  # 創建底部框架
bottom_frame.pack(side=tk.TOP, fill=tk.X)  # 將底部框架放置在窗口的頂部，並填滿 X 軸

# 定義不同數值範圍
ranges_spec = {
    '溫度': [(0, 20), (20, 40), (40, 100)],
    '濕度': [(0, 40), (40, 75), (75, 100)],
    '體溫': [(0, 25), (25, 37), (37, 45)],
    '心跳': [(0, 60), (60, 140), (140, 160)],
    'BMI': [(0, 18.5), (18.5, 24), (24, 27)]
}

top_values = ["溫度", "濕度", "體溫"]  # 頂部顯示的數值類型
bottom_values = ["心跳", "BMI"]  # 底部顯示的數值類型

# Google Sheets 連結
google_sheets_urls = {
    "溫度": "https://docs.google.com/spreadsheets/d/12rkfKKxrm3NcnrZNgZPzml9oNZm4alc2l-8UFsA2iCY/edit?resourcekey#gid=1685037583",
    "濕度": "https://docs.google.com/spreadsheets/d/12rkfKKxrm3NcnrZNgZPzml9oNZm4alc2l-8UFsA2iCY/edit?resourcekey#gid=1685037583",
    "體溫": "https://docs.google.com/spreadsheets/d/12rkfKKxrm3NcnrZNgZPzml9oNZm4alc2l-8UFsA2iCY/edit?resourcekey#gid=1685037583",
    "心跳": "https://docs.google.com/spreadsheets/d/1DUD0yMOqnjaZB5fhIytxBM0Ajmg6mP72oAmwC-grT4g/edit?resourcekey=&gid=1895836984#gid=1895836984",
    "BMI": "https://docs.google.com/spreadsheets/d/1ji-9bYlxt3KDxJvFIdat-3NwIkL7ejUa6wMFXgFe2a0/edit?resourcekey=&gid=1661867759#gid=1661867759"
}

needle_positions = []  # 存儲指針位置
canvases = []  # 存儲 Canvas

# 創建按鈕框架
button_frame = tk.Frame(main_window)
button_frame.pack(side=tk.TOP, fill=tk.X)

# 定義按鈕
buttons = [
    ("加入AI小幫手QR code", open_qr_code),
    ("統計圖示", open_looker_studio),  # 如果有其他功能，請替換 None
    ("Google Sheet連結", None),  # 如果有其他功能，請替換 None
    ("連線", connect_and_sync),
    ("異常事件紀錄", toggle_treeview),
]

# 創建並顯示按鈕
for text, command in buttons:
    button = tk.Button(button_frame, text=text, command=command)  # 創建按鈕
    button.pack(side=tk.LEFT, padx=2, pady=2)  # 將按鈕放置在按鈕框架中

time_label = tk.Label(main_window, font=("Arial", 16), padx=20, pady=10)  # 創建時間標籤
time_label.pack()  # 將時間標籤放置在主窗口中

treeview_frame = tk.Frame(main_window)  # 創建 Treeview 框架
treeview_frame.pack(fill=tk.BOTH, expand=True)  # 填滿整個窗口並擴展

# 創建 Treeview
tree = ttk.Treeview(treeview_frame, columns=("時間", "目前數值", "異常狀態"), show='headings')
tree.heading("時間", text="時間")  # 設置時間列標題
tree.heading("目前數值", text="目前數值")  # 設置目前數值列標題
tree.heading("異常狀態", text="異常狀態")  # 設置異常狀態列標題
tree.column("時間", width=150)  # 設置時間列寬度
tree.column("目前數值", width=150)  # 設置目前數值列寬度
tree.column("異常狀態", width=150)  # 設置異常狀態列寬度

tree.pack(fill=tk.BOTH, expand=True)  # 將 Treeview 添加到 Treeview 框架中

def get_latest_data():
    # 獲取最新數據
    queries = {
        '溫度': "SELECT 溫度 FROM dht11 ORDER BY 時間戳記 DESC LIMIT 1",
        '濕度': "SELECT 濕度 FROM dht11 ORDER BY 時間戳記 DESC LIMIT 1",
        '體溫': "SELECT 體溫 FROM dht11 ORDER BY 時間戳記 DESC LIMIT 1",
        '心跳': "SELECT 心跳 FROM heart_rate ORDER BY 時間戳記 DESC LIMIT 1",
        'BMI': "SELECT bmi FROM bmi ORDER BY 時間戳記 DESC LIMIT 1"
    }
    data = {key: None for key in queries.keys()}  # 初始化數據字典
    conn = pymysql.connect(host='localhost', port=3306, user='root', password='oneokrock12345', database='heart rate monitor')  # 連接資料庫
    cursor = conn.cursor()  # 創建游標
    for key, sql in queries.items():
        try:
            cursor.execute(sql)  # 執行查詢語句
            result = cursor.fetchone()  # 獲取查詢結果
            if result:
                data[key] = result[0]  # 更新數據字典
        except pymysql.Error as e:
            print(f"資料庫錯誤 ({key}): {e}")  # 捕獲並打印錯誤信息
    cursor.close()  # 關閉游標
    conn.close()  # 關閉連接
    return data  # 返回數據

def update_gauges():
    data = get_latest_data()
    for i, (key, value) in enumerate(data.items()):
        if value is not None and i < len(needle_positions):
            arrow, set_needle = needle_positions[i]
            new_arrow = set_needle(value)
            needle_positions[i] = (new_arrow, set_needle)
            
            # 更新指示燈
            ranges = ranges_spec[key]
            if is_high_or_low(value, ranges):
                green_buttons[i].pack_forget()
                red_buttons[i].pack(side=tk.LEFT, padx=2)
            else:
                red_buttons[i].pack_forget()
                green_buttons[i].pack(side=tk.LEFT, padx=2)
    
    for canvas in canvases:
        canvas.draw()
    
    main_window.after(1000, update_gauges)  # 每秒更新一次儀表盤
    
def create_and_add_gauge(value, frame):
    # 創建並添加儀表盤
    fig, ax = plt.subplots(figsize=(2.5, 2))  # 創建圖形
    ranges = ranges_spec[value]  # 獲取範圍
    needle, set_needle = create_gauge(fig, ax, ranges[0][0], ranges[-1][1], ranges)  # 創建儀表盤
    canvas, green_button, red_button = add_labels_and_buttons(frame, fig, ax, ranges, value, google_sheet_url=google_sheets_urls[value])  # 添加標籤和按鈕
    return needle, set_needle, canvas, green_button, red_button  # 返回指針、設置指針函數、Canvas、綠色按鈕和紅色按鈕

needle_positions = []  # 初始化指針位置列表
canvases = []  # 初始化 Canvas 列表
green_buttons = []  # 初始化綠色按鈕列表
red_buttons = []  # 初始化紅色按鈕列表

for i, value in enumerate(top_values + bottom_values):
    # 根據頂部和底部的數值類型創建儀表盤
    frame = top_frame if i < 3 else bottom_frame  # 根據索引選擇框架
    needle, set_needle, canvas, green_button, red_button = create_and_add_gauge(value, frame)  # 創建並添加儀表盤
    needle_positions.append((needle, set_needle))  # 添加指針位置
    canvases.append(canvas)  # 添加 Canvas
    green_buttons.append(green_button)  # 添加綠色按鈕
    red_buttons.append(red_button)  # 添加紅色按鈕
    
update_gauges()  # 更新儀表盤顯示
show_current_time()  # 啟動時間更新功能

main_window.mainloop()  # 啟動主循環
