# @Time : 2020/9/8 16:22
# @Author : Xuki
# @File : get_canny.py
# @Annotation :

import cv2


def nothing(x):
    print(x)
    pass


cv2.namedWindow('res')
cv2.createTrackbar('max', 'res', 0, 255, nothing)
cv2.createTrackbar('min', 'res', 0, 255, nothing)

img = cv2.imread('bank_card.jpg', 0)
# img = cv2.GaussianBlur(img, (3, 3), 0)


maxVal = 200
minVal = 100

# cv2.morphologyEx(img, cv2.MORPH_OPEN, (3, 3))

while True:
    if cv2.waitKey(20) & 0xFF == 27:
        break
    maxVal = cv2.getTrackbarPos('min', 'res')
    minVal = cv2.getTrackbarPos('max', 'res')
    if minVal < maxVal:
        edge = cv2.Canny(img, 100, 200)
        cv2.imshow('res', edge)
    else:
        edge = cv2.Canny(img, minVal, maxVal)
        cv2.imshow('res', edge)
cv2.destroyAllWindows()
