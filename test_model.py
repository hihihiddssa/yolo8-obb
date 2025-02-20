from ultralytics import YOLO
import cv2
import matplotlib.pyplot as plt
import os

def test_yolo_model(image_folder, model_path):
    # 加载模型
    model = YOLO(model_path)
    
    # 获取图片文件列表
    image_files = [f for f in os.listdir(image_folder) if f.endswith(('.png', '.jpg', '.jpeg'))]
    
    for image_file in image_files:
        image_path = os.path.join(image_folder, image_file)
        
        # 读取测试图片
        image = cv2.imread(image_path)
        if image is None:
            print(f"未找到图片文件: {image_path}")
            continue
        
        # 进行推理
        results = model(image)
        
        # 打印检测结果
        print(f"检测结果 ({image_file}):")
        for result in results:
            print(result)
        
        # 可视化检测结果
        for result in results:
            annotated_image = result.plot()  # 使用 plot() 方法获取带注释的图像
            plt.imshow(cv2.cvtColor(annotated_image, cv2.COLOR_BGR2RGB))
            plt.title(f"预测结果: {image_file}")
            plt.axis('off')
            plt.show()

if __name__ == "__main__":
    # 设置图片集文件夹路径和模型路径
    image_folder_path = 'D:/AMY_PROJECTS/yolo-dectect-teddy4/datasets_7d_x1y1/train/images'
    trained_model_path = 'D:/AMY_PROJECTS/yolo-dectect-teddy4/runs/train/exp3/weights/best.pt'
    
    # 测试模型
    test_yolo_model(image_folder_path, trained_model_path) 