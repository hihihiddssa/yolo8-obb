import cv2
import numpy as np
import os
import math

'''
#得到标注格式：0 cx cy w h angle
'''
class Annotator:
    def __init__(self, image_dir, save_dir, default_width=50):
        self.image_dir = image_dir
        self.save_dir = save_dir
        self.default_width = default_width
        self.current_width = default_width
        
        self.image = None
        self.image_name = ""
        self.drawing = False
        self.point1 = None
        self.point2 = None
        self.temp_point2 = None
        
        # 存储当前图片的所有标注
        self.annotations = []
        
        # 创建窗口和轨迹栏
        cv2.namedWindow('Annotator')
        cv2.createTrackbar('Width', 'Annotator', default_width, 200, self.width_callback)
    
    def width_callback(self, value):
        self.current_width = max(10, value)
        if self.point1 is not None:
            self.draw_image()
    
    def calculate_box_points(self, p1, p2, width):
        if p1 is None or p2 is None:
            return None
            
        # 计算中心线的方向向量
        dx = p2[0] - p1[0]
        dy = p2[1] - p1[1]
        length = math.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return None
            
        # 单位法向量
        nx = -dy/length
        ny = dx/length
        
        # 计算四个角点
        half_width = width/2
        points = np.array([
            [p1[0] + nx*half_width, p1[1] + ny*half_width],
            [p1[0] - nx*half_width, p1[1] - ny*half_width],
            [p2[0] - nx*half_width, p2[1] - ny*half_width],
            [p2[0] + nx*half_width, p2[1] + ny*half_width]
        ], dtype=np.float32)
        
        return points
    
    def draw_image(self):
        if self.image is None:
            return
            
        img_copy = self.image.copy()
        
        # 绘制已保存的标注
        for ann in self.annotations:
            p1, p2, width = ann
            points = self.calculate_box_points(p1, p2, width)
            if points is not None:
                # 绘制已保存的框（使用黄色）
                cv2.polylines(img_copy, [points.astype(np.int32)], True, (0, 255, 255), 2)
                # 绘制中心线
                cv2.line(img_copy, p1, p2, (255, 0, 0), 1)
                # 绘制端点
                cv2.circle(img_copy, p1, 3, (0, 255, 255), -1)
                cv2.circle(img_copy, p2, 3, (0, 255, 255), -1)
        
        # 绘制当前正在标注的框
        if self.point1 is not None:
            cv2.circle(img_copy, self.point1, 3, (0, 255, 0), -1)
            
            p2 = self.point2 if self.point2 is not None else self.temp_point2
            if p2 is not None:
                points = self.calculate_box_points(self.point1, p2, self.current_width)
                if points is not None:
                    # 绘制当前框（使用绿色）
                    cv2.polylines(img_copy, [points.astype(np.int32)], True, (0, 255, 0), 2)
                    # 绘制中心线
                    cv2.line(img_copy, self.point1, p2, (255, 0, 0), 1)
        
        cv2.imshow('Annotator', img_copy)
    
    def mouse_callback(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if not self.drawing:
                self.point1 = (x, y)
                self.drawing = True
                self.point2 = None
            else:
                self.point2 = (x, y)
                self.save_annotation()
                self.drawing = False
                self.point1 = None
                self.point2 = None
        
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            self.temp_point2 = (x, y)
            self.draw_image()
    
    def save_annotation(self):
        if self.point1 is None or self.point2 is None:
            return
            
        points = self.calculate_box_points(self.point1, self.point2, self.current_width)
        if points is None:
            return
            
        # 保存标注点到内存
        self.annotations.append((self.point1, self.point2, self.current_width))
        
        # 转换为YOLO-OBB格式 (cx, cy, w, h, angle)
        h, w = self.image.shape[:2]
        
        # 计算中心点
        cx = (self.point1[0] + self.point2[0]) / 2 / w
        cy = (self.point1[1] + self.point2[1]) / 2 / h
        
        # 计算宽度和高度
        box_width = self.current_width / w
        box_height = math.sqrt((self.point2[0]-self.point1[0])**2 + 
                             (self.point2[1]-self.point1[1])**2) / h
        
        # 计算角度（弧度）
        angle = math.atan2(self.point2[1]-self.point1[1], 
                          self.point2[0]-self.point1[0])
        
        # 保存标注到文件
        label_path = os.path.join(self.save_dir, 
                                 os.path.splitext(self.image_name)[0] + '.txt')
        with open(label_path, 'a') as f:
            f.write(f"0 {cx:.6f} {cy:.6f} {box_width:.6f} {box_height:.6f} {angle:.6f}\n")
    
    def load_annotations(self):
        """加载已有的标注"""
        self.annotations = []
        label_path = os.path.join(self.save_dir, 
                                 os.path.splitext(self.image_name)[0] + '.txt')
        if os.path.exists(label_path):
            h, w = self.image.shape[:2]
            with open(label_path, 'r') as f:
                for line in f:
                    parts = line.strip().split()
                    if len(parts) == 6:  # class_id, cx, cy, width, height, angle
                        cx = float(parts[1]) * w
                        cy = float(parts[2]) * h
                        width = float(parts[3]) * w
                        height = float(parts[4]) * h
                        angle = float(parts[5])
                        
                        # 从中心点、宽度、高度和角度重建两个端点
                        dx = height * math.cos(angle)
                        dy = height * math.sin(angle)
                        p1 = (int(cx - dx/2), int(cy - dy/2))
                        p2 = (int(cx + dx/2), int(cy + dy/2))
                        
                        self.annotations.append((p1, p2, width))
    
    def undo_last_annotation(self):
        """撤销最后一个标注"""
        if self.annotations:
            self.annotations.pop()
            label_path = os.path.join(self.save_dir, 
                                    os.path.splitext(self.image_name)[0] + '.txt')
            if os.path.exists(label_path):
                with open(label_path, 'r') as f:
                    lines = f.readlines()
                if lines:
                    with open(label_path, 'w') as f:
                        f.writelines(lines[:-1])
            self.draw_image()
    
    def run(self):
        cv2.setMouseCallback('Annotator', self.mouse_callback)
        
        image_files = [f for f in os.listdir(self.image_dir) 
                      if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        
        for image_name in image_files:
            self.image_name = image_name
            image_path = os.path.join(self.image_dir, image_name)
            self.image = cv2.imread(image_path)
            if self.image is None:
                continue
                
            self.point1 = None
            self.point2 = None
            self.drawing = False
            
            # 加载已有标注
            self.load_annotations()
            self.draw_image()
            
            while True:
                self.draw_image()
                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):  # 退出程序
                    return
                elif key == ord('n'):  # 下一张图片
                    break
                elif key == ord('z'):  # 撤销上一次标注
                    self.undo_last_annotation()
                    
        cv2.destroyAllWindows()

if __name__ == "__main__":
    # 设置图片目录和标注保存目录
    image_dir = "rgb"  # 替换为你的图片目录
    save_dir = "labels"   # 替换为你的标注保存目录
    
    # 创建保存目录
    os.makedirs(save_dir, exist_ok=True)
    
    # 启动标注程序
    annotator = Annotator(image_dir, save_dir)
    annotator.run() 