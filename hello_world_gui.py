
import tkinter as tk
from tkinter import messagebox

def show_hello():
    """显示Hello World消息"""
    messagebox.showinfo("Greetings", "Hello, World!")

# 创建主窗口
root = tk.Tk()
root.title("Hello World Application")
root.geometry("300x200")

# 创建标签
label = tk.Label(root, text="Welcome to Hello World GUI!", font=("Arial", 12))
label.pack(pady=20)

# 创建按钮
button = tk.Button(root, text="Click Me!", command=show_hello, font=("Arial", 10))
button.pack(pady=10)

# 创建退出按钮
exit_button = tk.Button(root, text="Exit", command=root.quit, font=("Arial", 10))
exit_button.pack(pady=10)

# 运行主循环
root.mainloop()
