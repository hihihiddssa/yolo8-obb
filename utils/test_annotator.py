import cv2
import numpy as np
import os

def draw_box(img, points, color=(0, 255, 0), thickness=2):
    # 将归一化坐标转换为实际像素坐标
    h, w = img.shape[:2]
    points = points.reshape((-1, 2))
    points[:, 0] *= w
    points[:, 1] *= h
    points = points.astype(np.int32)
    
    # 画出四边形
    cv2.polylines(img, [points], True, color, thickness)
    return img

def process_image(img_path, txt_path):
    # 读取图像
    img = cv2.imread(img_path)
    if img is None:
        print(f"无法读取图像: {img_path}")
        return
    
    # 读取txt文件
    try:
        with open(txt_path, 'r') as f:
            line = f.readline().strip()
            values = list(map(float, line.split()))
            # 第一个值是类别，后面8个值是4个点的坐标
            points = np.array(values[1:]).reshape(4, 2)
    except Exception as e:
        print(f"读取标注文件出错: {txt_path}")
        print(e)
        return
    
    # 画框
    result = draw_box(img.copy(), points)
    
    # 显示结果
    cv2.imshow('Result', result)
    cv2.waitKey(0)

def main():
    # 指定目录路径
    directory = 'D:/AMY_PROJECTS/yolo-dectect-teddy4/rgb'
    
    # 获取所有png文件
    for filename in os.listdir(directory):
        if filename.endswith('.png'):
            img_path = os.path.join(directory, filename)
            txt_path = os.path.join(directory, filename.replace('.png', '.txt'))
            
            if os.path.exists(txt_path):
                print(f"处理: {filename}")
                process_image(img_path, txt_path)

if __name__ == "__main__":
    main()
    cv2.destroyAllWindows()