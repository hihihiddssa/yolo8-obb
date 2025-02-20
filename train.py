from ultralytics import YOLO
import os
import yaml
from pathlib import Path

def train_yolo_obb():
    """
    训练YOLOv8 OBB模型
    """
    # 训练配置
    config = {
        'model_type': 'yolov8s-obb.pt',  # 使用YOLOv8s OBB预训练模型
        'epochs': 100,                    # 训练轮数
        'batch_size': 16,                 # 批次大小
        'imgsz': 640,                     # 图片大小
        'data_yaml': 'data.yaml',         # 数据集配置文件
        'device': 'cuda:0',               # 使用的设备（GPU）
        'project': 'runs/train',          # 保存训练结果的目录
        'name': 'exp3',                    # 实验名称
        'save': True,                     # 保存模型
        'save_period': 10,                # 每10个epoch保存一次
        'patience': 50,                   # early stopping patience
    }
    
    # 检查data.yaml是否存在
    if not os.path.exists(config['data_yaml']):
        raise FileNotFoundError(f"未找到数据集配置文件: {config['data_yaml']}")
    
    # 加载数据集配置确认是OBB模式
    with open(config['data_yaml'], 'r', encoding='utf-8') as f:
        data_config = yaml.safe_load(f)
        if not data_config.get('obb', False):
            raise ValueError("data.yaml中未设置obb=True，请确保启用OBB模式")
    
    # 使用本地的预训练模型
    model_path = 'D:/AMY_PROJECTS/yolo-dectect-teddy4/weights/yolo11n-obb.pt'
    if not Path(model_path).exists():
        raise FileNotFoundError(f"模型文件 {model_path} 不存在，请确认文件路径正确")
        
    model = YOLO(model_path)
    print(f"成功加载预训练模型: {model_path}")
    
    # 开始训练
    try:
        results = model.train(
            data=config['data_yaml'],
            epochs=config['epochs'],
            imgsz=config['imgsz'],
            batch=config['batch_size'],
            device=config['device'],
            project=config['project'],
            name=config['name'],
            save=config['save'],
            save_period=config['save_period'],
            patience=config['patience'],
            verbose=True,
            pretrained=True,
            optimizer='auto',
            lr0=0.01,                 # 初始学习率
            lrf=0.01,                 # 最终学习率
            momentum=0.937,           # SGD动量
            weight_decay=0.0005,      # 权重衰减
            warmup_epochs=3,          # 预热轮数
            warmup_momentum=0.8,      # 预热动量
            warmup_bias_lr=0.1,       # 预热偏置学习率
            box=7.5,                  # 框损失增益
            cls=0.5,                  # 分类损失增益
            dfl=1.5,                  # DFL损失增益
            pose=12.0,               # 姿态损失增益（用于OBB）
            plots=True,               # 绘制训练图表
        )
        
        print("训练完成！")
        print(f"最佳模型保存在: {Path(config['project']) / config['name'] / 'weights/best.pt'}")
        return results
        
    except Exception as e:
        print(f"训练过程中出现错误: {str(e)}")
        raise

if __name__ == "__main__":
    # 训练模型
    train_yolo_obb()