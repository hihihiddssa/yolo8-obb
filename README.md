# YOLOv8 旋转目标检测项目 🎯

这是一个基于YOLOv8的旋转目标检测（OBB）项目。 🚀

## ✨ 项目特点

- 🔥 使用YOLOv8-OBB进行旋转目标检测
- 📚 支持6D和7D两种标注格式
- 🛠️ 提供完整的标注和测试工具链
- 📊 支持多种数据格式转换

## 💻 环境要求

- 🐍 Python 3.7+
- 🔧 ultralytics
- 👁️ OpenCV (cv2)
- 📈 matplotlib
- 🔥 PyTorch
- 📦 PyYAML

## 📁 项目结构

```
yolo8-obb/
├── datasets_6d_cxcy/       # 6D格式数据集
│   └── train/
│       ├── images/         # 训练图片
│       └── labels/         # 标签(类别,中心点,宽高,角度)
│   └── val/               # 验证集
├── datasets_7d_x1y1/       # 7D格式数据集
│   ├── train/
│   │   ├── images/        # 训练图片
│   │   └── labels/        # 标签(类别,四点坐标)
│   └── val/               # 验证集
├── rgb/                    # 原始图片目录。包含图片类别和标注的4个点的坐标。
├── labels/                 # 标注文件保存目录
├── utils/
│   ├── annotator.py       # 标注工具
│   ├── test_annotator.py  # 标注测试工具
│   └── convert_7d_to_6d.py # 格式转换工具
├── train.py               # 训练脚本
├── test_model.py          # 测试脚本
└── data.yaml              # 数据集配置
```

## 📝 数据格式说明

### 6D格式 (datasets_6d_cxcy) 📦
- 格式：`class_id cx cy w h angle`
- 说明：
  - class_id: 类别ID（0）
  - cx, cy: 中心点坐标（归一化）
  - w, h: 宽度和高度（归一化）
  - angle: 旋转角度（弧度）
- 用途：数据标注输出格式

### 7D格式 (datasets_7d_x1y1) 📦+
- 格式：`class_id x1 y1 x2 y2 x3 y3 x4 y4`
- 说明：
  - class_id: 类别ID（0）
  - (x1,y1)~(x4,y4): 四个顶点坐标（归一化）
- 用途：YOLO训练输入格式

## 🛠️ 工具使用说明

### 标注工具 (annotator.py)

1. 准备工作：
   - 将图片放入 `rgb` 文件夹
   - 运行：`python utils/annotator.py`

2. 操作方法：
   - 左键点击：确定起点
   - 移动鼠标：调整方向和长度
   - 再次左键：完成标注
   - 滑动条：调整框宽度
   - 快捷键：
     - 'z': 撤销
     - 'n': 下一张
     - 'q': 退出

### 格式转换
使用 `utils/convert_7d_to_6d.py` 转换格式

## 📖 训练流程

1. 准备数据：
   - 使用标注工具标注图片
   - 转换为对应格式
   - 整理数据集目录结构

2. 配置 data.yaml：
```yaml
path: 数据集路径
train: train/images
val: val/images
nc: 1
names: ['teddy']
obb: True  # 启用旋转框检测
```

3. 开始训练：
```bash
python train.py
```

## 🔍 测试模型

运行测试脚本：
```bash
python test_model.py
```

## ⚠️ 注意事项

- 📌 标注时保持方向一致性
- 💾 使用正确的模型权重文件
- 🚀 推荐使用GPU训练
- 🔄 确认数据格式匹配

## 📬 联系方式

[您的联系方式]
