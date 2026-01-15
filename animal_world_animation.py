

import tkinter as tk
import random
import math
import time

class AnimalWorldAnimation:
    def __init__(self, root):
        self.root = root
        self.root.title("动物世界动画")
        self.root.geometry("800x600")
        self.root.configure(bg='sky blue')

        # 创建画布
        self.canvas = tk.Canvas(root, width=800, height=600, bg='light blue')
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # 动物列表
        self.animals = []

        # 创建地面
        self.canvas.create_rectangle(0, 500, 800, 600, fill='forest green', outline='forest green')

        # 添加太阳
        self.canvas.create_oval(650, 50, 750, 150, fill='yellow', outline='orange')

        # 添加云朵
        self.clouds = []
        for i in range(3):
            x = 100 + i * 250
            cloud = self.canvas.create_oval(x, 80, x+60, 140, fill='white', outline='white')
            self.clouds.append(cloud)

        # 添加树木
        for i in range(5):
            x = 50 + i * 150
            self.canvas.create_rectangle(x, 450, x+20, 500, fill='saddle brown', outline='saddle brown')
            self.canvas.create_oval(x-30, 420, x+50, 480, fill='forest green', outline='forest green')

        # 天气系统
        self.weather = 'sunny'  # sunny, rainy, snowy
        self.weather_effects = []

        # 创建控制面板
        self.btn_frame = tk.Frame(root, bg='sky blue')
        self.btn_frame.pack(pady=10)

        # 动物选择下拉菜单
        tk.Label(self.btn_frame, text="选择动物:", bg='sky blue', font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.animal_var = tk.StringVar(value="随机")
        animal_options = ["随机", "大象", "狮子", "长颈鹿", "猴子", "熊猫", "老虎", "兔子", "斑马"]
        self.animal_menu = tk.OptionMenu(self.btn_frame, self.animal_var, *animal_options)
        self.animal_menu.config(font=("Arial", 10))
        self.animal_menu.pack(side=tk.LEFT, padx=5)

        self.add_animal_btn = tk.Button(self.btn_frame, text="添加动物", command=self.add_selected_animal, font=("Arial", 12))
        self.add_animal_btn.pack(side=tk.LEFT, padx=5)

        self.start_btn = tk.Button(self.btn_frame, text="开始动画", command=self.start_animation, font=("Arial", 12))
        self.start_btn.pack(side=tk.LEFT, padx=5)

        self.stop_btn = tk.Button(self.btn_frame, text="停止动画", command=self.stop_animation, font=("Arial", 12))
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # 天气控制按钮
        self.weather_frame = tk.Frame(root, bg='sky blue')
        self.weather_frame.pack(pady=5)

        tk.Label(self.weather_frame, text="天气:", bg='sky blue', font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        self.sunny_btn = tk.Button(self.weather_frame, text="晴天", command=lambda: self.change_weather('sunny'), font=("Arial", 10))
        self.sunny_btn.pack(side=tk.LEFT, padx=3)

        self.rainy_btn = tk.Button(self.weather_frame, text="雨天", command=lambda: self.change_weather('rainy'), font=("Arial", 10))
        self.rainy_btn.pack(side=tk.LEFT, padx=3)

        self.snowy_btn = tk.Button(self.weather_frame, text="雪天", command=lambda: self.change_weather('snowy'), font=("Arial", 10))
        self.snowy_btn.pack(side=tk.LEFT, padx=3)

        # 动画控制变量
        self.is_animating = False
        self.animation_id = None

    def add_animal(self, animal_type=None):
        """添加动物"""
        animal_types = ['elephant', 'lion', 'giraffe', 'monkey', 'panda', 'tiger', 'rabbit', 'zebra']
        if animal_type is None:
            animal_type = random.choice(animal_types)
        else:
            animal_type = animal_type.strip()

        # 随机位置（在地面以上）
        x = random.randint(50, 750)
        y = random.randint(400, 480)

        # 创建动物（更真实的设计）
        if animal_type == 'elephant':
            # 大象身体
            body = self.canvas.create_oval(x-25, y-20, x+25, y+15, fill='#A9A9A9', outline='#696969')
            # 大象头部
            head = self.canvas.create_oval(x+15, y-25, x+40, y-5, fill='#A9A9A9', outline='#696969')
            # 象鼻（曲线）
            trunk = self.canvas.create_line(x+40, y-15, x+50, y-5, x+52, y+5, fill='#A9A9A9', width=5, smooth=True)
            # 象牙
            tusk1 = self.canvas.create_line(x+35, y-8, x+40, y-3, fill='white', width=2)
            tusk2 = self.canvas.create_line(x+35, y-12, x+40, y-7, fill='white', width=2)
            # 四条腿
            leg1 = self.canvas.create_rectangle(x-20, y+10, x-12, y+25, fill='#808080', outline='#696969')
            leg2 = self.canvas.create_rectangle(x-5, y+10, x+3, y+25, fill='#808080', outline='#696969')
            leg3 = self.canvas.create_rectangle(x+8, y+10, x+16, y+25, fill='#808080', outline='#696969')
            leg4 = self.canvas.create_rectangle(x+20, y+8, x+28, y+23, fill='#808080', outline='#696969')
            # 眼睛
            eye = self.canvas.create_oval(x+25, y-20, x+30, y-15, fill='black')
            # 耳朵
            ear1 = self.canvas.create_oval(x+5, y-28, x+20, y-10, fill='#A9A9A9', outline='#696969')
            ear2 = self.canvas.create_oval(x+25, y-28, x+40, y-10, fill='#A9A9A9', outline='#696969')
            # 尾巴
            tail = self.canvas.create_line(x-25, y, x-30, y+5, x-28, y+10, fill='#808080', width=2)
            animal_obj = {'type': 'elephant', 'parts': [leg1, leg2, leg3, leg4, body, head, ear1, ear2, trunk, tusk1, tusk2, eye, tail], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        elif animal_type == 'lion':
            # 狮子身体
            body = self.canvas.create_oval(x-22, y-15, x+15, y+12, fill='#DAA520', outline='#B8860B')
            # 四条腿
            leg1 = self.canvas.create_rectangle(x-18, y+8, x-12, y+22, fill='#CD853F', outline='#B8860B')
            leg2 = self.canvas.create_rectangle(x-5, y+8, x+1, y+22, fill='#CD853F', outline='#B8860B')
            leg3 = self.canvas.create_rectangle(x+5, y+8, x+11, y+22, fill='#CD853F', outline='#B8860B')
            leg4 = self.canvas.create_rectangle(x+12, y+8, x+18, y+22, fill='#CD853F', outline='#B8860B')
            # 狮子头部
            head = self.canvas.create_oval(x+10, y-20, x+35, y+5, fill='#DAA520', outline='#B8860B')
            # 鬃毛（多层）
            mane1 = self.canvas.create_oval(x+5, y-28, x+40, y+8, fill='#8B4513', outline='#654321')
            mane2 = self.canvas.create_oval(x+8, y-25, x+37, y+5, fill='#A0522D', outline='#654321')
            # 耳朵
            ear1 = self.canvas.create_polygon(x+12, y-20, x+15, y-28, x+18, y-20, fill='#CD853F', outline='#B8860B')
            ear2 = self.canvas.create_polygon(x+27, y-20, x+30, y-28, x+33, y-20, fill='#CD853F', outline='#B8860B')
            # 眼睛
            eye1 = self.canvas.create_oval(x+17, y-12, x+21, y-8, fill='yellow', outline='black')
            eye2 = self.canvas.create_oval(x+25, y-12, x+29, y-8, fill='yellow', outline='black')
            pupil1 = self.canvas.create_oval(x+18, y-11, x+20, y-9, fill='black')
            pupil2 = self.canvas.create_oval(x+26, y-11, x+28, y-9, fill='black')
            # 鼻子
            nose = self.canvas.create_oval(x+20, y-6, x+26, y-2, fill='#8B4513')
            # 嘴巴
            mouth = self.canvas.create_line(x+23, y-2, x+20, y+1, x+26, y+1, fill='#654321', width=1)
            # 尾巴
            tail = self.canvas.create_line(x-22, y, x-30, y-5, fill='#CD853F', width=3)
            tail_tuft = self.canvas.create_oval(x-33, y-8, x-27, y-2, fill='#8B4513', outline='#654321')
            animal_obj = {'type': 'lion', 'parts': [leg1, leg2, leg3, leg4, body, mane1, mane2, head, ear1, ear2, eye1, eye2, pupil1, pupil2, nose, mouth, tail, tail_tuft], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        elif animal_type == 'giraffe':
            # 长颈鹿身体
            body = self.canvas.create_oval(x-18, y-25, x+18, y+10, fill='#FFD700', outline='#DAA520')
            # 四条腿（细长）
            leg1 = self.canvas.create_rectangle(x-14, y+5, x-9, y+28, fill='#F4A460', outline='#DAA520')
            leg2 = self.canvas.create_rectangle(x-3, y+5, x+2, y+28, fill='#F4A460', outline='#DAA520')
            leg3 = self.canvas.create_rectangle(x+5, y+5, x+10, y+28, fill='#F4A460', outline='#DAA520')
            leg4 = self.canvas.create_rectangle(x+11, y+5, x+16, y+28, fill='#F4A460', outline='#DAA520')
            # 长颈鹿脖子（长方形）
            neck = self.canvas.create_rectangle(x+8, y-55, x+18, y-25, fill='#FFD700', outline='#DAA520')
            # 长颈鹿头部
            head = self.canvas.create_oval(x+5, y-65, x+25, y-50, fill='#FFD700', outline='#DAA520')
            # 角（两个小突起）
            horn1 = self.canvas.create_rectangle(x+10, y-68, x+12, y-65, fill='#8B4513', outline='#654321')
            horn2 = self.canvas.create_rectangle(x+18, y-68, x+20, y-65, fill='#8B4513', outline='#654321')
            horn_ball1 = self.canvas.create_oval(x+9, y-70, x+13, y-66, fill='#654321')
            horn_ball2 = self.canvas.create_oval(x+17, y-70, x+21, y-66, fill='#654321')
            # 耳朵
            ear1 = self.canvas.create_oval(x+7, y-62, x+11, y-58, fill='#F4A460', outline='#DAA520')
            ear2 = self.canvas.create_oval(x+19, y-62, x+23, y-58, fill='#F4A460', outline='#DAA520')
            # 眼睛
            eye1 = self.canvas.create_oval(x+10, y-60, x+13, y-57, fill='black')
            eye2 = self.canvas.create_oval(x+17, y-60, x+20, y-57, fill='black')
            # 鼻子和嘴
            nose = self.canvas.create_oval(x+12, y-54, x+18, y-52, fill='#8B4513')
            mouth = self.canvas.create_line(x+15, y-52, x+15, y-50, fill='#654321', width=1)
            # 斑点（多个）
            spots = []
            for i in range(8):
                sx = x + random.randint(-15, 15)
                sy = y + random.randint(-20, 5)
                spot = self.canvas.create_oval(sx, sy, sx+5, sy+5, fill='#8B4513', outline='#8B4513')
                spots.append(spot)
            # 尾巴
            tail = self.canvas.create_line(x-18, y-5, x-25, y, fill='#F4A460', width=2)
            tail_tuft = self.canvas.create_oval(x-28, y-2, x-24, y+2, fill='#654321', outline='#654321')
            # 鬃毛
            mane = self.canvas.create_line(x+13, y-50, x+13, y-30, fill='#8B4513', width=2)
            animal_obj = {'type': 'giraffe', 'parts': [leg1, leg2, leg3, leg4, body, neck, head, horn1, horn2, horn_ball1, horn_ball2, ear1, ear2, eye1, eye2, nose, mouth] + spots + [tail, tail_tuft, mane], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        elif animal_type == 'monkey':
            # 猴子身体
            body = self.canvas.create_oval(x-15, y-12, x+12, y+12, fill='#8B4513', outline='#654321')
            # 四肢
            arm1 = self.canvas.create_line(x-12, y-8, x-20, y-5, fill='#8B4513', width=4)
            arm2 = self.canvas.create_line(x+9, y-8, x+17, y-5, fill='#8B4513', width=4)
            leg1 = self.canvas.create_line(x-10, y+8, x-15, y+20, fill='#8B4513', width=4)
            leg2 = self.canvas.create_line(x+7, y+8, x+12, y+20, fill='#8B4513', width=4)
            # 手和脚
            hand1 = self.canvas.create_oval(x-23, y-7, x-17, y-3, fill='#D2691E', outline='#8B4513')
            hand2 = self.canvas.create_oval(x+14, y-7, x+20, y-3, fill='#D2691E', outline='#8B4513')
            foot1 = self.canvas.create_oval(x-18, y+18, x-12, y+22, fill='#D2691E', outline='#8B4513')
            foot2 = self.canvas.create_oval(x+9, y+18, x+15, y+22, fill='#D2691E', outline='#8B4513')
            # 猴子头部
            head = self.canvas.create_oval(x-12, y-28, x+12, y-10, fill='#8B4513', outline='#654321')
            # 脸部
            face = self.canvas.create_oval(x-8, y-24, x+8, y-14, fill='#D2691E', outline='#8B4513')
            # 眼睛
            eye1 = self.canvas.create_oval(x-5, y-22, x-2, y-19, fill='white', outline='black')
            eye2 = self.canvas.create_oval(x+2, y-22, x+5, y-19, fill='white', outline='black')
            pupil1 = self.canvas.create_oval(x-4, y-21, x-3, y-20, fill='black')
            pupil2 = self.canvas.create_oval(x+3, y-21, x+4, y-20, fill='black')
            # 耳朵
            ear1 = self.canvas.create_oval(x-13, y-24, x-9, y-20, fill='#D2691E', outline='#8B4513')
            ear2 = self.canvas.create_oval(x+9, y-24, x+13, y-20, fill='#D2691E', outline='#8B4513')
            # 鼻子
            nose = self.canvas.create_oval(x-2, y-18, x+2, y-16, fill='#654321')
            # 嘴巴
            mouth = self.canvas.create_arc(x-4, y-18, x+4, y-14, start=200, extent=140, fill='#654321', outline='#654321')
            # 长尾巴（曲线）
            tail = self.canvas.create_line(x-15, y+5, x-22, y+10, x-20, y+18, fill='#8B4513', width=3, smooth=True)
            animal_obj = {'type': 'monkey', 'parts': [arm1, arm2, leg1, leg2, hand1, hand2, foot1, foot2, body, head, face, ear1, ear2, eye1, eye2, pupil1, pupil2, nose, mouth, tail], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        elif animal_type == 'panda':
            # 熊猫身体
            body = self.canvas.create_oval(x-20, y-18, x+20, y+15, fill='white', outline='black', width=2)
            # 四条腿（黑色）
            leg1 = self.canvas.create_rectangle(x-16, y+10, x-9, y+25, fill='black', outline='black')
            leg2 = self.canvas.create_rectangle(x-3, y+10, x+4, y+25, fill='black', outline='black')
            leg3 = self.canvas.create_rectangle(x+6, y+10, x+13, y+25, fill='black', outline='black')
            leg4 = self.canvas.create_rectangle(x+14, y+8, x+21, y+23, fill='black', outline='black')
            # 熊猫头部
            head = self.canvas.create_oval(x+8, y-30, x+35, y-5, fill='white', outline='black', width=2)
            # 黑色耳朵（圆形）
            ear1 = self.canvas.create_oval(x+10, y-32, x+18, y-24, fill='black', outline='black')
            ear2 = self.canvas.create_oval(x+25, y-32, x+33, y-24, fill='black', outline='black')
            # 眼睛（黑色圆圈）
            eye_patch1 = self.canvas.create_oval(x+12, y-23, x+20, y-13, fill='black', outline='black')
            eye_patch2 = self.canvas.create_oval(x+23, y-23, x+31, y-13, fill='black', outline='black')
            # 白色眼球
            eyeball1 = self.canvas.create_oval(x+14, y-20, x+18, y-16, fill='white')
            eyeball2 = self.canvas.create_oval(x+25, y-20, x+29, y-16, fill='white')
            # 黑色瞳孔
            pupil1 = self.canvas.create_oval(x+15, y-19, x+17, y-17, fill='black')
            pupil2 = self.canvas.create_oval(x+26, y-19, x+28, y-17, fill='black')
            # 鼻子
            nose = self.canvas.create_oval(x+19, y-14, x+24, y-10, fill='black')
            # 嘴巴
            mouth_left = self.canvas.create_line(x+21, y-10, x+18, y-8, fill='black', width=2)
            mouth_right = self.canvas.create_line(x+21, y-10, x+24, y-8, fill='black', width=2)
            # 短尾巴（白色）
            tail = self.canvas.create_oval(x-23, y, x-17, y+6, fill='white', outline='black')
            # 前肢（黑色）
            arm1 = self.canvas.create_oval(x-18, y-8, x-10, y+8, fill='black', outline='black')
            arm2 = self.canvas.create_oval(x+12, y-5, x+20, y+10, fill='black', outline='black')
            animal_obj = {'type': 'panda', 'parts': [leg1, leg2, leg3, leg4, body, arm1, arm2, head, ear1, ear2, eye_patch1, eye_patch2, eyeball1, eyeball2, pupil1, pupil2, nose, mouth_left, mouth_right, tail], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        elif animal_type == 'tiger':
            # 老虎身体
            body = self.canvas.create_oval(x-25, y-18, x+20, y+13, fill='#FF8C00', outline='#8B4500')
            # 四条腿
            leg1 = self.canvas.create_rectangle(x-20, y+8, x-13, y+25, fill='#FF8C00', outline='#8B4500')
            leg2 = self.canvas.create_rectangle(x-6, y+8, x+1, y+25, fill='#FF8C00', outline='#8B4500')
            leg3 = self.canvas.create_rectangle(x+6, y+8, x+13, y+25, fill='#FF8C00', outline='#8B4500')
            leg4 = self.canvas.create_rectangle(x+15, y+8, x+22, y+25, fill='#FF8C00', outline='#8B4500')
            # 老虎头部
            head = self.canvas.create_oval(x+12, y-28, x+40, y-5, fill='#FF8C00', outline='#8B4500')
            # 白色脸颊
            cheek1 = self.canvas.create_oval(x+14, y-18, x+22, y-10, fill='white', outline='#8B4500')
            cheek2 = self.canvas.create_oval(x+30, y-18, x+38, y-10, fill='white', outline='#8B4500')
            # 眼睛
            eye1 = self.canvas.create_oval(x+18, y-20, x+22, y-16, fill='yellow', outline='black')
            eye2 = self.canvas.create_oval(x+30, y-20, x+34, y-16, fill='yellow', outline='black')
            pupil1 = self.canvas.create_oval(x+19, y-19, x+21, y-17, fill='black')
            pupil2 = self.canvas.create_oval(x+31, y-19, x+33, y-17, fill='black')
            # 鼻子
            nose = self.canvas.create_polygon(x+24, y-15, x+26, y-13, x+28, y-15, fill='#FF1493', outline='black')
            # 嘴巴
            mouth = self.canvas.create_arc(x+20, y-15, x+32, y-10, start=200, extent=140, outline='black', width=2)
            # 胡须
            whisker1 = self.canvas.create_line(x+14, y-14, x+8, y-13, fill='black', width=1)
            whisker2 = self.canvas.create_line(x+14, y-12, x+8, y-12, fill='black', width=1)
            whisker3 = self.canvas.create_line(x+38, y-14, x+44, y-13, fill='black', width=1)
            whisker4 = self.canvas.create_line(x+38, y-12, x+44, y-12, fill='black', width=1)
            # 耳朵
            ear1 = self.canvas.create_polygon(x+15, y-28, x+18, y-33, x+21, y-28, fill='#FF8C00', outline='black')
            ear2 = self.canvas.create_polygon(x+31, y-28, x+34, y-33, x+37, y-28, fill='#FF8C00', outline='black')
            ear_inner1 = self.canvas.create_polygon(x+16, y-28, x+18, y-31, x+20, y-28, fill='white')
            ear_inner2 = self.canvas.create_polygon(x+32, y-28, x+34, y-31, x+36, y-28, fill='white')
            # 身体条纹
            stripes = []
            stripe_positions = [(-20, -10), (-15, -5), (-10, 0), (-5, 5), (0, -8), (5, -3), (10, 2)]
            for sx, sy in stripe_positions:
                stripe = self.canvas.create_line(x+sx, y+sy, x+sx+3, y+sy+8, fill='black', width=3)
                stripes.append(stripe)
            # 头部条纹
            head_stripe1 = self.canvas.create_line(x+20, y-24, x+22, y-20, fill='black', width=2)
            head_stripe2 = self.canvas.create_line(x+30, y-24, x+32, y-20, fill='black', width=2)
            stripes.extend([head_stripe1, head_stripe2])
            # 尾巴
            tail = self.canvas.create_line(x-25, y-5, x-35, y-10, x-38, y-5, fill='#FF8C00', width=4, smooth=True)
            tail_stripe1 = self.canvas.create_line(x-28, y-8, x-30, y-6, fill='black', width=2)
            tail_stripe2 = self.canvas.create_line(x-33, y-9, x-35, y-7, fill='black', width=2)
            animal_obj = {'type': 'tiger', 'parts': [leg1, leg2, leg3, leg4, body] + stripes + [head, cheek1, cheek2, ear1, ear2, ear_inner1, ear_inner2, eye1, eye2, pupil1, pupil2, nose, mouth, whisker1, whisker2, whisker3, whisker4, tail, tail_stripe1, tail_stripe2], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        elif animal_type == 'rabbit':
            # 兔子身体
            body = self.canvas.create_oval(x-15, y-10, x+15, y+12, fill='white', outline='#D3D3D3')
            # 四条腿
            leg1 = self.canvas.create_oval(x-12, y+8, x-6, y+18, fill='white', outline='#D3D3D3')
            leg2 = self.canvas.create_oval(x-2, y+8, x+4, y+18, fill='white', outline='#D3D3D3')
            leg3 = self.canvas.create_oval(x+5, y+8, x+11, y+18, fill='white', outline='#D3D3D3')
            leg4 = self.canvas.create_oval(x+12, y+8, x+18, y+18, fill='white', outline='#D3D3D3')
            # 兔子头部
            head = self.canvas.create_oval(x+8, y-20, x+28, y-2, fill='white', outline='#D3D3D3')
            # 长耳朵（椭圆形）
            ear1 = self.canvas.create_oval(x+10, y-40, x+16, y-18, fill='white', outline='#D3D3D3')
            ear2 = self.canvas.create_oval(x+20, y-40, x+26, y-18, fill='white', outline='#D3D3D3')
            # 耳朵内部（粉色）
            ear_inner1 = self.canvas.create_oval(x+11, y-37, x+15, y-22, fill='#FFB6C1', outline='#FFB6C1')
            ear_inner2 = self.canvas.create_oval(x+21, y-37, x+25, y-22, fill='#FFB6C1', outline='#FFB6C1')
            # 眼睛
            eye1 = self.canvas.create_oval(x+12, y-15, x+16, y-11, fill='black')
            eye2 = self.canvas.create_oval(x+20, y-15, x+24, y-11, fill='black')
            # 鼻子（三角形）
            nose = self.canvas.create_polygon(x+18, y-10, x+16, y-7, x+20, y-7, fill='#FFB6C1')
            # 嘴巴（Y形）
            mouth1 = self.canvas.create_line(x+18, y-7, x+16, y-5, fill='#D3D3D3', width=1)
            mouth2 = self.canvas.create_line(x+18, y-7, x+20, y-5, fill='#D3D3D3', width=1)
            # 胡须
            whisker1 = self.canvas.create_line(x+10, y-9, x+4, y-10, fill='#A9A9A9', width=1)
            whisker2 = self.canvas.create_line(x+10, y-8, x+4, y-8, fill='#A9A9A9', width=1)
            whisker3 = self.canvas.create_line(x+26, y-9, x+32, y-10, fill='#A9A9A9', width=1)
            whisker4 = self.canvas.create_line(x+26, y-8, x+32, y-8, fill='#A9A9A9', width=1)
            # 短尾巴（圆球状）
            tail = self.canvas.create_oval(x-18, y+2, x-12, y+8, fill='white', outline='#D3D3D3')
            # 前爪
            paw1 = self.canvas.create_oval(x-10, y+3, x-4, y+9, fill='white', outline='#D3D3D3')
            paw2 = self.canvas.create_oval(x+8, y+3, x+14, y+9, fill='white', outline='#D3D3D3')
            animal_obj = {'type': 'rabbit', 'parts': [leg1, leg2, leg3, leg4, body, paw1, paw2, head, ear1, ear2, ear_inner1, ear_inner2, eye1, eye2, nose, mouth1, mouth2, whisker1, whisker2, whisker3, whisker4, tail], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        elif animal_type == 'zebra':
            # 斑马身体
            body = self.canvas.create_oval(x-22, y-16, x+18, y+12, fill='white', outline='black', width=2)
            # 四条腿
            leg1 = self.canvas.create_rectangle(x-18, y+8, x-12, y+25, fill='white', outline='black')
            leg2 = self.canvas.create_rectangle(x-6, y+8, x, y+25, fill='white', outline='black')
            leg3 = self.canvas.create_rectangle(x+4, y+8, x+10, y+25, fill='white', outline='black')
            leg4 = self.canvas.create_rectangle(x+12, y+8, x+18, y+25, fill='white', outline='black')
            # 腿上的条纹
            leg_stripe1a = self.canvas.create_line(x-18, y+12, x-12, y+12, fill='black', width=2)
            leg_stripe1b = self.canvas.create_line(x-18, y+18, x-12, y+18, fill='black', width=2)
            leg_stripe2a = self.canvas.create_line(x-6, y+12, x, y+12, fill='black', width=2)
            leg_stripe2b = self.canvas.create_line(x-6, y+18, x, y+18, fill='black', width=2)
            leg_stripe3a = self.canvas.create_line(x+4, y+12, x+10, y+12, fill='black', width=2)
            leg_stripe3b = self.canvas.create_line(x+4, y+18, x+10, y+18, fill='black', width=2)
            leg_stripe4a = self.canvas.create_line(x+12, y+12, x+18, y+12, fill='black', width=2)
            leg_stripe4b = self.canvas.create_line(x+12, y+18, x+18, y+18, fill='black', width=2)
            # 斑马头部
            head = self.canvas.create_oval(x+12, y-25, x+35, y-5, fill='white', outline='black', width=2)
            # 脖子
            neck = self.canvas.create_polygon(x+10, y-18, x+18, y-25, x+18, y-10, fill='white', outline='black')
            # 鬃毛（黑色）
            mane1 = self.canvas.create_line(x+12, y-25, x+14, y-28, fill='black', width=2)
            mane2 = self.canvas.create_line(x+15, y-26, x+17, y-29, fill='black', width=2)
            mane3 = self.canvas.create_line(x+18, y-26, x+20, y-29, fill='black', width=2)
            # 耳朵
            ear1 = self.canvas.create_polygon(x+15, y-25, x+17, y-30, x+19, y-25, fill='white', outline='black')
            ear2 = self.canvas.create_polygon(x+26, y-25, x+28, y-30, x+30, y-25, fill='white', outline='black')
            # 眼睛
            eye1 = self.canvas.create_oval(x+18, y-20, x+22, y-16, fill='black')
            eye2 = self.canvas.create_oval(x+26, y-20, x+30, y-16, fill='black')
            # 鼻子
            nose = self.canvas.create_oval(x+28, y-13, x+33, y-10, fill='black')
            # 嘴巴
            mouth = self.canvas.create_line(x+30, y-10, x+28, y-8, x+32, y-8, fill='black', width=1)
            # 身体条纹（多条）
            body_stripes = []
            stripe_positions = [(-18, -12), (-14, -8), (-10, -4), (-6, 0), (-2, 4), (2, -10), (6, -6), (10, -2), (14, 2)]
            for sx, sy in stripe_positions:
                stripe = self.canvas.create_line(x+sx, y+sy-5, x+sx, y+sy+8, fill='black', width=3)
                body_stripes.append(stripe)
            # 头部条纹
            head_stripe1 = self.canvas.create_line(x+20, y-22, x+22, y-18, fill='black', width=2)
            head_stripe2 = self.canvas.create_line(x+24, y-21, x+26, y-17, fill='black', width=2)
            head_stripe3 = self.canvas.create_line(x+28, y-20, x+30, y-16, fill='black', width=2)
            body_stripes.extend([head_stripe1, head_stripe2, head_stripe3])
            # 尾巴
            tail = self.canvas.create_line(x-22, y-5, x-30, y-8, fill='black', width=2)
            tail_tuft = self.canvas.create_line(x-30, y-10, x-32, y-12, x-28, y-12, fill='black', width=2)
            animal_obj = {'type': 'zebra', 'parts': [leg1, leg2, leg3, leg4, leg_stripe1a, leg_stripe1b, leg_stripe2a, leg_stripe2b, leg_stripe3a, leg_stripe3b, leg_stripe4a, leg_stripe4b, body, neck] + body_stripes + [head, mane1, mane2, mane3, ear1, ear2, eye1, eye2, nose, mouth, tail, tail_tuft], 'x': x, 'y': y, 'dx': random.choice([-2, -1, 1, 2])}
        else:
            return

        self.animals.append(animal_obj)

    def add_selected_animal(self):
        """根据下拉菜单选择添加动物"""
        animal_map = {
            "随机": None,
            "大象": "elephant",
            "狮子": "lion",
            "长颈鹿": "giraffe",
            "猴子": "monkey",
            "熊猫": "panda",
            "老虎": "tiger",
            "兔子": "rabbit",
            "斑马": "zebra"
        }
        selected = self.animal_var.get()
        animal_type = animal_map.get(selected, None)
        self.add_animal(animal_type)

    def change_weather(self, weather_type):
        """切换天气"""
        self.weather = weather_type
        # 清除现有天气效果
        for effect in self.weather_effects:
            self.canvas.delete(effect)
        self.weather_effects = []

        # 更新背景颜色
        if weather_type == 'sunny':
            self.canvas.configure(bg='light blue')
        elif weather_type == 'rainy':
            self.canvas.configure(bg='light gray')
            # 创建雨滴效果
            for i in range(50):
                x = random.randint(0, 800)
                y = random.randint(0, 500)
                raindrop = self.canvas.create_line(x, y, x, y+10, fill='blue', width=1)
                self.weather_effects.append(raindrop)
        elif weather_type == 'snowy':
            self.canvas.configure(bg='lightsteelblue')
            # 创建雪花效果
            for i in range(40):
                x = random.randint(0, 800)
                y = random.randint(0, 500)
                snowflake = self.canvas.create_oval(x, y, x+5, y+5, fill='white', outline='white')
                self.weather_effects.append(snowflake)

    def check_collisions(self):
        """检查动物之间的碰撞"""
        for i, animal1 in enumerate(self.animals):
            for animal2 in self.animals[i+1:]:
                # 简单的距离碰撞检测
                dx = animal1['x'] - animal2['x']
                dy = animal1['y'] - animal2['y']
                distance = math.sqrt(dx*dx + dy*dy)

                # 如果距离小于40像素，认为发生碰撞
                if distance < 40:
                    # 交换方向
                    animal1['dx'], animal2['dx'] = animal2['dx'], animal1['dx']
                    # 添加短暂的跳跃效果表示碰撞
                    for part in animal1['parts']:
                        self.canvas.move(part, 0, -3)
                    for part in animal2['parts']:
                        self.canvas.move(part, 0, -3)
                    self.root.after(100, lambda a1=animal1, a2=animal2:
                        [self.canvas.move(part, 0, 3) for part in a1['parts']] +
                        [self.canvas.move(part, 0, 3) for part in a2['parts']])

    def start_animation(self):
        """开始动画"""
        if not self.is_animating:
            self.is_animating = True
            self.animate()

    def stop_animation(self):
        """停止动画"""
        self.is_animating = False
        if self.animation_id:
            self.root.after_cancel(self.animation_id)

    def animate(self):
        """动画循环"""
        if self.is_animating:
            # 移动动物
            for animal in self.animals:
                # 更新位置
                animal['x'] += animal['dx']

                # 边界检查和方向反转
                if animal['x'] <= 20 or animal['x'] >= 780:
                    animal['dx'] = -animal['dx']

                # 移动所有图形元素
                for part in animal['parts']:
                    self.canvas.move(part, animal['dx'], 0)

                # 随机跳跃效果
                if random.random() < 0.02:  # 2% 概率跳跃
                    for part in animal['parts']:
                        self.canvas.move(part, 0, -5)
                    # 200ms 后落地
                    self.root.after(200, lambda a=animal: [self.canvas.move(part, 0, 5) for part in a['parts']])

            # 检查动物碰撞
            self.check_collisions()

            # 移动云朵
            for cloud in self.clouds:
                self.canvas.move(cloud, 0.5, 0)
                # 重置云朵位置
                coords = self.canvas.coords(cloud)
                if coords[0] > 800:
                    self.canvas.move(cloud, -900, 0)

            # 更新天气效果
            if self.weather == 'rainy':
                for raindrop in self.weather_effects:
                    self.canvas.move(raindrop, 0, 5)
                    coords = self.canvas.coords(raindrop)
                    if coords[1] > 600:
                        self.canvas.move(raindrop, 0, -600)
            elif self.weather == 'snowy':
                for snowflake in self.weather_effects:
                    self.canvas.move(snowflake, random.uniform(-0.5, 0.5), 2)
                    coords = self.canvas.coords(snowflake)
                    if coords[1] > 600:
                        self.canvas.move(snowflake, 0, -600)
                        self.canvas.coords(snowflake, random.randint(0, 800), coords[1]-600,
                                         random.randint(0, 800)+5, coords[3]-600)

            # 继续动画循环
            self.animation_id = self.root.after(50, self.animate)

def main():
    root = tk.Tk()
    app = AnimalWorldAnimation(root)
    root.mainloop()

if __name__ == "__main__":
    main()

