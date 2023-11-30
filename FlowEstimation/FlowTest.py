import os
import cv2
import numpy as np
from tkinter import Tk, filedialog

# Open a file dialog to choose the input image
Tk().withdraw()  # We don't want a full GUI, so keep the root window from appearing
input_image_path = filedialog.askopenfilename(title="Select an Image")

# Check if a file was selected
if not input_image_path:
    print("No file selected. Exiting.")
    exit()

# Read the selected input image
image = cv2.imread(input_image_path)

# 複製一份原始圖像
image_with_arrows = image.copy()

# 將圖像轉換為灰階
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 計算梯度
sobelx = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=13)
sobely = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=13)

# 計算梯度方向和大小
magnitude, angle = cv2.cartToPolar(sobelx, sobely, angleInDegrees=True)

# 將角度轉換為弧度
angle_rad = np.radians(angle)

# 計算箭頭的終點座標
arrow_length = 20
x2 = np.cos(angle_rad) * arrow_length
y2 = np.sin(angle_rad) * arrow_length

# 定義區域大小
region_size = 30

# 在每個區域上計算平均方向並畫箭頭
for i in range(0, gray_image.shape[0], region_size):
    for j in range(0, gray_image.shape[1], region_size):
        x1, y1 = j, i
        x2_avg, y2_avg = np.mean(x2[i:i+region_size, j:j+region_size]), np.mean(y2[i:i+region_size, j:j+region_size])
        x2_rounded, y2_rounded = int(round(x2_avg)), int(round(y2_avg))
        # 調整箭頭寬度
        thickness = 1
        line_type = 4
        shift = 0
        tip_length = 2.5
        cv2.arrowedLine(image_with_arrows, (x1, y1), (x1 + x2_rounded, y1 + y2_rounded), (0, 0, 255), thickness, line_type, shift, tip_length)

# 顯示並保存原始彩色圖片和箭頭表示的運動方向
# Get the filename without extension from the input image path
filename_without_extension = os.path.splitext(os.path.basename(input_image_path))[0]

# Save the result with a filename based on the input image
output_filename = f'result_with_arrows_{filename_without_extension}.png'
cv2.imshow('Original Image with Arrows', image_with_arrows)
cv2.imwrite(output_filename, image_with_arrows)
cv2.waitKey(0)
cv2.destroyAllWindows()
