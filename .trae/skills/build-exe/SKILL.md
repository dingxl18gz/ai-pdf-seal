---
name: "build-exe"
description: "Builds a standalone Windows executable using PyInstaller. Invoke when user wants to package the app as an exe."
---

# Build Exe

This skill builds a standalone .exe file from the Python project using PyInstaller.

## What It Does

1. Installs PyInstaller if not already installed
2. Runs PyInstaller with appropriate options
3. Generates a standalone `ai-pdf-seal.exe` in the `dist/` folder

## Requirements

- PyInstaller package
- All dependencies listed in pyproject.toml

## Usage

### GUI 版本（推荐）
打包 GUI 版本，运行时无控制台窗口：
1. Run: `pip install pyinstaller` (if needed)
2. Run: `pyinstaller --onefile --windowed --name ai-pdf-seal --add-data "config.yaml;." main_gui.py`
3. Output: `dist/ai-pdf-seal.exe`

### 命令行版本
打包命令行版本，保留控制台窗口：
1. Run: `pip install pyinstaller` (if needed)
2. Run: `pyinstaller --onefile --name ai-pdf-seal --add-data "config.yaml;." main.py`
3. Output: `dist/ai-pdf-seal.exe`

## Technical Details

- Output: Single file executable (~30MB)
- Includes: Python interpreter, all dependencies, config.yaml
- Platform: Windows
- No Python installation required to run the exe
