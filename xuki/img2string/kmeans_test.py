# @Time : 2020/9/10 11:43
# @Author : Xuki
# @File : kmeans_test.py
# @Annotation : 

import cv2
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import smtplib
from email.mime.text import MIMEText


def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()


# labels = np.repeat(np.arange(10), 3)[..., None]
# print(labels)
# exit(0)

data = np.random.randint(10, size=20)
print(data)
print(np.argwhere(data > 2)[0])
# data = np.isnan(data).any()
# data = np.unique(data, return_counts=True)
exit(0)
image = cv2.imread('zjz.jpeg')
b, g, r = cv2.split(image)
b = b.flatten()
print(b)
# bin = np.bincount(b)
# print(bin)
# hist = cv2.calcHist([image], [0], None, [256], [0, 256])
# print(hist.flatten())
plt.hist(b, 256, [0, 256])
plt.show()
exit(0)

image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
cells = [np.hsplit(rows, 3) for rows in np.vsplit(image, 5)]
cells = np.array(cells)
print(cells.shape)
img = np.hstack(cells[0, :])
print(img.shape)
cv_show('split', img)

knn = cv2.ml.KNearest_create()
knn.train(cv2.ml.ROW_SAMPLE)
knn.findNearest()
exit(0)

cv_show('image_xor', cv2.add(image, image))

mask = np.random.choice(np.array([0, 255], dtype=np.uint8), image.shape)
image_xor = cv2.bitwise_xor(image, mask)
cv_show('image_xor', image_xor)

cv_show('image_xor', cv2.bitwise_xor(image_xor, mask))

img_1 = cv2.imread('kmeans.jpg')
img_2 = cv2.imread('zjz.jpeg')
# cv_show('img', cv2.add(img_1, img_2))
cv_show('img', cv2.addWeighted(img_1, 0.7, img_2, 0.3, 0))

print(3 & 5)
a = np.ones((3, 3), dtype=np.uint8) * 5
b = np.ones((3, 3), dtype=np.uint8) * 3
d = cv2.bitwise_and(a, b)
print(d)
exit(0)

d = np.random.choice([0, 255], (100, 100, 3))
d = d.astype(np.uint8)
print(d)
cv_show('d', d)
exit(0)

img_1 = np.full((100, 100, 3), 255, dtype=np.uint8)
img_2 = np.full((100, 100, 3), 255, dtype=np.uint8)
# mask = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
mask = np.eye(100, dtype=np.uint8)
# mask[mask == 1] = 255
# print(mask)
# cv_show('mask', mask)
dst = cv2.bitwise_and(img_1, img_2)
print(dst)
# cv_show('dst', dst)
# cv_show('+++++', img_1 + img_2)
print(dst)
exit(0)

a = np.arange(0, 27).reshape((3, 3, 3))
print(a[:, 1:2, 2])
print(a[..., 2])
print((a > 1) & (a < 4))
print(a > 2)
exit(0)
a = np.random.randint(1, 100, (3, 3, 2))
print(a)
# print(a[:, ..., 1])
# print(a[1, ..., 1])
print(a[1, 1, ...])
exit(0)


# pd.set_option('display.max_columns', None)
# 显示所有行
# pd.set_option('display.max_rows', None)


def seg_kmeans_gray():
    img = cv2.imread('kmeans.jpg', cv2.IMREAD_GRAYSCALE)

    # 展平
    img_flat = img.reshape((img.shape[0] * img.shape[1], 1))
    img_flat = np.float32(img_flat)

    # 迭代参数
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 20, 0.5)
    flags = cv2.KMEANS_RANDOM_CENTERS

    # 聚类
    compactness, labels, centers = cv2.kmeans(img_flat, 4, None, criteria, 10, flags)

    # 显示结果
    img_output = labels.reshape((img.shape[0], img.shape[1]))

    # img_output = pd.DataFrame(img_output)

    # img_output = img_output.applymap(lambda x: x if x == 1 else 0)

    # print(img_output.apply(pd.value_counts))

    # 颜色label
    color = np.uint8([[255, 0, 0],
                      [0, 0, 255],
                      [128, 128, 128],
                      [0, 255, 0]])
    res = color[labels.flatten()]
    # 显示
    result = res.reshape((cv2.imread('kmeans.jpg').shape))

    plt.subplot(131), plt.imshow(img, 'gray'), plt.title('input')
    plt.subplot(132), plt.imshow(img_output, 'gray'), plt.title('kmeans')
    plt.subplot(133), plt.imshow(result), plt.title('kmeans')
    plt.show()


if __name__ == '__main__':
    seg_kmeans_gray()
