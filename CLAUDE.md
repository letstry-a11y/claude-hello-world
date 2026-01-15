# Project: Claude Hello World

## Overview
This is a Python learning project demonstrating progression from basic "Hello World" programs to complex GUI animations.

## Project Structure
```
├── hello_world.py          # Basic Python print example
├── hello_world.js          # Basic JavaScript console.log example
├── hello_world.html        # Basic HTML page
├── hello_world_gui.py      # Simple tkinter GUI application
├── animal_world_animation.py   # Main project: Animal World Animation
├── run_animation.bat       # Batch script to launch animation
└── 动物世界动画使用说明书.md    # User manual (Chinese)
```

## Tech Stack
- **Language**: Python 3.x
- **GUI Framework**: tkinter
- **Runtime**: Anaconda Python (`D:\Anaconda\python.exe`)

## Main Application: Animal World Animation
Features:
- 8 animal types: elephant, lion, giraffe, monkey, panda, tiger, rabbit, zebra
- Weather system: sunny, rainy, snowy
- Animation effects: movement, jumping, collision detection
- Interactive controls for adding animals and changing weather

## Development Guidelines
- Use Chinese for UI labels and user-facing text
- Follow tkinter Canvas-based drawing patterns
- Animation loop uses 50ms intervals via `root.after()`
- Each animal is composed of multiple geometric shapes stored in a parts list

## Running the Project
```bash
python animal_world_animation.py
# or
run_animation.bat
```
