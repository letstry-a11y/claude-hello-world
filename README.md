# Claude Hello World

Python 学习项目，从基础的 "Hello World" 程序逐步进阶到复杂的 GUI 动画应用和实用工具开发。

## 项目结构

```
├── hello_world.py              # Python 基础打印示例
├── hello_world.js              # JavaScript 控制台示例
├── hello_world.html            # HTML 页面示例
├── hello_world_gui.py          # tkinter GUI 应用
├── animal_world_animation.py   # 动物世界动画
├── robot_arm_kinematics.cpp    # 机械臂运动学程序
├── run_animation.bat           # 动画启动脚本
├── 动物世界动画使用说明书.md     # 动画使用手册
│
├── html_to_pptx.py             # HTML 转 PowerPoint 转换器 (新)
├── create_pptx.py              # Anthropic API 创建 PPT (新)
├── list_skills.py              # Anthropic Skills 列表工具 (新)
├── skywalker_report.html       # 示例 HTML 报告模板 (新)
└── HTML转PPT转换器说明.md       # 转换器使用说明 (新)
```

## 技术栈

- **语言**: Python 3.x, JavaScript, C++
- **GUI 框架**: tkinter
- **文档处理**: python-pptx, BeautifulSoup4
- **运行环境**: Anaconda Python

---

## 应用一：动物世界动画

基于 tkinter 的交互式动画应用。

**功能特点**：
- 8 种动物类型：大象、狮子、长颈鹿、猴子、熊猫、老虎、兔子、斑马
- 天气系统：晴天、雨天、雪天
- 动画效果：移动、跳跃、碰撞检测
- 交互控制：添加动物、切换天气

**运行方式**：
```bash
python animal_world_animation.py
# 或
run_animation.bat
```

---

## 应用二：HTML 转 PowerPoint 转换器

将 HTML 文件转换为 PowerPoint 演示文稿的实用工具。

**功能特点**：
- 自动检测幻灯片分隔（slide-container、section、hr 等）
- 支持多种内容类型（标题、列表、图片、表格、卡片布局）
- FontAwesome 图标自动转换为 Unicode 符号
- 自定义主题颜色
- GUI 图形界面 + 命令行双模式

**运行方式**：
```bash
# GUI 模式
python html_to_pptx.py

# 命令行模式
python html_to_pptx.py input.html output.pptx
```

**安装依赖**：
```bash
pip install python-pptx beautifulsoup4 requests
```

**打包为 EXE**：
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "HTML转PPT转换器" html_to_pptx.py
```

详细说明请参阅 [HTML转PPT转换器说明.md](HTML转PPT转换器说明.md)

---

## 应用三：Anthropic API 工具

使用 Anthropic Claude API 的辅助工具。

| 文件 | 说明 |
|-----|------|
| `create_pptx.py` | 使用 Anthropic PPTX Skill 自动生成演示文稿 |
| `list_skills.py` | 列出可用的 Anthropic Skills |

**使用前提**：
```bash
pip install anthropic
export ANTHROPIC_API_KEY=your-api-key
```

---

## 许可证

MIT License
