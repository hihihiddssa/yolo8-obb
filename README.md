# 📦 YOLOv8-OBB Object Detection

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![YOLOv8](https://img.shields.io/badge/YOLO-v8.0-red.svg)](https://github.com/ultralytics/ultralytics)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

YOLOv8-OBB-based object detection project, supporting detection and coordinate conversion for grasping tasks.  
基于 YOLOv8-OBB 的物体检测项目，支持通过检测结果进行抓取点坐标转换，助力自动化抓取任务。

---

## 🌟 Features / 功能亮点

- 📐 Oriented Bounding Box (OBB) detection 支持旋转边界框检测
- 🤖 Grasp point extraction & coordinate transformation 可提取抓取点并实现坐标转换
- ⚡ Fast & accurate detection 检测速度快、精度高
- 🔄 Easy integration, flexible extension 易于集成与扩展

---

## 🚀 Quick Start / 快速开始

1. **Clone the repository / 克隆代码库**
    ```bash
    git clone https://github.com/hihihiddssa/yolo8-obb.git
    cd yolo8-obb
    ```

2. **Install dependencies / 安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3. **Prepare model weights / 准备模型权重**
    - Download YOLOv8-OBB weights and place in `weights/` folder  
      下载 YOLOv8-OBB 权重文件并放入 `weights/` 目录

4. **Run detection / 运行检测**
    ```bash
    python main.py --image test.jpg
    ```

---

## 🔧 Project Structure / 项目结构

```
yolo8-obb/
├── main.py
├── requirements.txt
├── README.md
├── weights/                 # 模型权重文件
├── screenshots/             # 项目截图
├── utils/                   # 工具函数
└── ...
```

---

## 📦 Dependencies / 依赖说明

- Python 3.8+
- YOLOv8 (Ultralytics)
- OpenCV
- Numpy
- 其它依赖见 `requirements.txt`

---

## 💡 Contribution / 贡献方式

Feel free to submit [Issues](https://github.com/hihihiddssa/yolo8-obb/issues) or [Pull Requests](https://github.com/hihihiddssa/yolo8-obb/pulls) to improve the project.  
欢迎提交 Issue 或 Pull Request 改进本项目功能！

---

## 📄 License / 许可证

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.  
本项目采用 MIT 许可证，详情见 LICENSE 文件。

---

## ✨ Author / 作者

- [hihihiddssa](https://github.com/hihihiddssa)

---

# 📦 YOLOv8-OBB 物体检测

基于 YOLOv8-OBB 的物体检测项目，能够检测物体并支持后续抓取点坐标转换，适用于自动化抓取、智能制造等场景。

## 🌟 功能亮点

- 📐 支持旋转边界框（OBB）检测
- 🤖 可提取抓取点并进行坐标转换
- ⚡ 检测速度快，精度高
- 🔄 易于集成与扩展

## 🖼️ 项目截图

> 请将项目截图添加到 `screenshots/` 目录，并在此引用。

![检测示例](screenshots/detection_example.png)
![抓取点](screenshots/grasp_point.png)

## 🚀 快速开始

1. **克隆代码库**
    ```bash
    git clone https://github.com/hihihiddssa/yolo8-obb.git
    cd yolo8-obb
    ```

2. **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3. **准备模型权重**
    - 下载 YOLOv8-OBB 权重文件并放入 `weights/` 目录

4. **运行检测**
    ```bash
    python main.py --image test.jpg
    ```

## 🔧 项目结构

```
yolo8-obb/
├── main.py
├── requirements.txt
├── README.md
├── weights/                 # 模型权重文件
├── screenshots/             # 项目截图
├── utils/                   # 工具函数
└── ...
```

## 📦 依赖说明

- Python 3.8+
- YOLOv8 (Ultralytics)
- OpenCV
- Numpy
- 其它依赖见 `requirements.txt`

## 💡 贡献方式

欢迎提交 Issue 或 Pull Request 改进本项目功能！

## 📄 许可证

本项目采用 MIT 许可证，详情见 LICENSE 文件。

## ✨ 作者 agacila@outlook.com

- [hihihiddssa](https://github.com/hihihiddssa)

---
