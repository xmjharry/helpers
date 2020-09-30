# @Time : 2020/9/10 14:45
# @Author : Xuki
# @File : img_cutout.py
# @Annotation : 

import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
import pandas as pd


def cv_show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    # cv2.destroyAllWindows()


image = cv.imread('zjz.jpeg')

rows, cols = image.shape[:2]

map_x = np.zeros((rows, cols), dtype=np.float32)
map_y = np.zeros((rows, cols), dtype=np.float32)

for i in range(rows):
    for j in range(cols):
        if 0.25 * rows < i < 0.75 * rows and 0.25 * cols < j < 0.75 * cols:
            map_x.itemset((i, j), 2 * (j - cols * 0.25) + 0.5)
            map_y.itemset((i, j), 2 * (i - rows * 0.25) + 0.5)
rst = cv.remap(image, map_x, map_y, cv.INTER_LINEAR)
cv_show('rst', rst)
exit(0)

purle = np.array([255, 0, 255])
# b, g, r = cv.split(image)
# image = cv.merge([r, g, b])
cv.imshow("input", image)
h, w, ch = image.shape
# 构建图像数据
data = image.reshape((-1, 3))
data = np.float32(data)

# 图像分割
criteria = (cv.TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER, 10, 1.0)
num_clusters = 4
ret, label, center = cv.kmeans(data, num_clusters, None, criteria, num_clusters, cv.KMEANS_RANDOM_CENTERS)
print(center)
exit(0)

# 生成mask区域
index = label[0][0]
# center = np.uint8(center)
# color = center[0]
mask = np.full((h, w), 255, dtype=np.uint8)
label = np.reshape(label, (h, w))
# alpha图
mask[label == index] = 0

# 高斯模糊
se = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))
# 膨胀，防止背景出现
cv.erode(mask, se, mask)
# 边缘模糊
mask = cv.GaussianBlur(mask, (5, 5), 0)
cv.imshow('alpha-image', mask)

# 白色背景
bg = np.full(image.shape, 255, dtype=np.uint8)

# 粉丝背景
purple = np.array([255, 0, 255])
bg_color = np.tile(purple, (image.shape[0], image.shape[1], 1))

alpha = mask.astype(np.float32) / 255.
# 切片还可以包括省略号 …，来使选择元组的长度与数组的维度相同。 如果在行位置使用省略号，它将返回包含行中元素的 ndarray。
# [:,None]简单说就是说它增加了一个维度
fg = alpha[..., None] * image
cv.imshow('fg', fg.astype(np.uint8))
new_image = fg + (1 - alpha[..., None]) * bg
new_image_purple = fg + (1 - alpha[..., None]) * bg_color

# plt.subplot(121), plt.imshow(np.hstack((image, new_image.astype(np.uint8)))), plt.title('white')
# plt.subplot(122), plt.imshow(np.hstack((image, new_image_purle.astype(np.uint8)))), plt.title('purle')
# plt.show()

cv.imwrite("white.jpg", np.hstack((image, new_image.astype(np.uint8))))
cv.imwrite("purple.jpg", np.hstack((image, new_image_purple.astype(np.uint8))))
cv.waitKey(0)
cv.destroyAllWindows()
