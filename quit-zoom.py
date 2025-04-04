import tkinter as tk
from tkinter import ttk
import os
import threading
import time

# 退出 Zoom 的函数
def exit_zoom():
    try:
        os.system("taskkill /IM Zoom.exe /F")
    except Exception as e:
        print(f"无法关闭 Zoom: {e}")

# 主窗口类
class ZoomExitApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Zoom 退出提醒")
        self.root.geometry("500x250")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)  # 窗口置顶
        
        # 倒计时初始值
        self.countdown = 30
        self.running = True
        self.delay_active = False
        
        # 创建界面
        self.create_widgets()
        
        # 启动倒计时线程
        self.start_countdown_thread()

    def create_widgets(self):
        # 主提示文字
        self.label = tk.Label(self.root, text="将在以下时间后退出 Zoom：", font=("Segoe UI", 12))
        self.label.pack(pady=20)

        # 倒计时显示
        self.time_label = tk.Label(self.root, text=f"{self.countdown} 秒", font=("Segoe UI", 14, "bold"))
        self.time_label.pack(pady=10)

        # 按钮框架
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)

        # 确定按钮
        self.ok_button = tk.Button(button_frame, text="确定", command=self.confirm_exit, width=10, font=("Segoe UI", 10))
        self.ok_button.grid(row=0, column=0, padx=10)

        # 推迟按钮和下拉菜单
        self.delay_options = ["10 分钟", "30 分钟", "1 小时"]
        self.delay_var = tk.StringVar(value=self.delay_options[0])
        self.delay_menu = ttk.Combobox(button_frame, textvariable=self.delay_var, values=self.delay_options, state="readonly", width=12, font=("Segoe UI", 10))
        self.delay_menu.grid(row=0, column=1, padx=10)

        self.delay_button = tk.Button(button_frame, text="推迟", command=self.delay_exit, width=10, font=("Segoe UI", 10))
        self.delay_button.grid(row=0, column=2, padx=10)

        # 取消按钮
        self.cancel_button = tk.Button(button_frame, text="取消", command=self.cancel_exit, width=10, font=("Segoe UI", 10))
        self.cancel_button.grid(row=0, column=3, padx=10)

    def start_countdown_thread(self):
        if hasattr(self, 'thread') and self.thread.is_alive():
            return  # 如果线程已在运行，不重复启动
        self.thread = threading.Thread(target=self.update_countdown)
        self.thread.daemon = True
        self.thread.start()

    def update_countdown(self):
        while self.running and self.countdown >= 0:
            self.update_time_label()
            time.sleep(1)
            self.countdown -= 1
        if self.countdown < 0 and self.running:
            self.time_label.config(text=f"现在关闭zoom")
            exit_zoom()
            self.time_label.config(text=f"zoom已关闭，程序退出中。。。")
            time.sleep(2)
            self.root.quit()

    # 更新倒计时显示的方法
    def update_time_label(self):
        minutes, seconds = divmod(self.countdown, 60)
        if minutes > 0:
            self.time_label.config(text=f"{minutes} 分钟 {seconds} 秒")
        else:
            self.time_label.config(text=f"{seconds} 秒")

    def confirm_exit(self):
        self.running = False
        exit_zoom()
        self.root.quit()

    def delay_exit(self):
        # 获取推迟时间并转换为秒
        delay_time = self.delay_var.get()
        if delay_time == "10 分钟":
            seconds = 10 * 60
        elif delay_time == "30 分钟":
            seconds = 30 * 60
        else:  # "1 小时"
            seconds = 60 * 60
        
        # 重置倒计时
        self.countdown = seconds
        self.delay_active = True
        self.update_time_label()
        
        # 如果线程已结束，重新启动
        if not self.thread.is_alive():
            self.running = True
            self.start_countdown_thread()

    def cancel_exit(self):
        self.running = False
        self.root.quit()

# 主程序入口
if __name__ == "__main__":
    root = tk.Tk()
    app = ZoomExitApp(root)
    root.mainloop()