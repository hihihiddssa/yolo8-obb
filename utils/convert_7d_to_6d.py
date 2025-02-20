import os
import shutil
import numpy as np
from pathlib import Path

def points_to_obb(points):
    """将4个点转换为中心点、宽高、角度格式
    points: [(x1,y1), (x2,y2), (x3,y3), (x4,y4)]
    return: cx, cy, w, h, angle
    """
    # 转换为numpy数组
    points = np.array(points).reshape(4, 2)
    
    # 计算中心点
    center = np.mean(points, axis=0)
    cx, cy = center
    
    # 计算主方向
    vec = points[1] - points[0]
    angle = np.arctan2(vec[1], vec[0])
    
    # 确保角度在-pi/2到pi/2之间
    while angle > np.pi/2:
        angle -= np.pi
    while angle < -np.pi/2:
        angle += np.pi
    
    # 计算宽高
    width = np.linalg.norm(points[1] - points[0])
    height = np.linalg.norm(points[2] - points[1])
    
    return cx, cy, width, height, angle

def convert_label(input_path, output_path):
    """转换单个标签文件"""
    with open(input_path, 'r') as f:
        lines = f.readlines()
    
    converted_lines = []
    for line in lines:
        values = list(map(float, line.strip().split()))
        class_id = int(values[0])
        points = [(values[i], values[i+1]) for i in range(1, 9, 2)]
        
        cx, cy, w, h, angle = points_to_obb(points)
        converted_line = f"{class_id} {cx:.6f} {cy:.6f} {w:.6f} {h:.6f} {angle:.6f}\n"
        converted_lines.append(converted_line)
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w') as f:
        f.writelines(converted_lines)

def convert_dataset(input_root, output_root):
    """转换整个数据集"""
    # 创建输出目录
    os.makedirs(output_root, exist_ok=True)
    
    # 处理训练集和验证集
    for split in ['train', 'val']:
        # 复制图片
        src_img_dir = os.path.join(input_root, split, 'images')
        dst_img_dir = os.path.join(output_root, split, 'images')
        if os.path.exists(src_img_dir):
            shutil.copytree(src_img_dir, dst_img_dir, dirs_exist_ok=True)
        
        # 转换标签
        src_label_dir = os.path.join(input_root, split, 'labels')
        dst_label_dir = os.path.join(output_root, split, 'labels')
        
        if os.path.exists(src_label_dir):
            for label_file in os.listdir(src_label_dir):
                if label_file.endswith('.txt'):
                    src_path = os.path.join(src_label_dir, label_file)
                    dst_path = os.path.join(dst_label_dir, label_file)
                    convert_label(src_path, dst_path)

if __name__ == "__main__":
    # 设置输入输出路径
    input_dataset = "datasets_7d_x1y1"
    output_dataset = "datasets_6d_cxcy"
    
    # 执行转换
    convert_dataset(input_dataset, output_dataset)
    print(f"数据集转换完成！\n从 {input_dataset} 转换到 {output_dataset}") 