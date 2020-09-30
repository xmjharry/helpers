# @Time : 2020/9/14 17:16
# @Author : Xuki
# @File : get_bank_card_num.py
# @Annotation : 


import cv2 as cv


def cv_show(name, img):
    cv.imshow(name, img)
    cv.waitKey(0)
    # cv2.destroyAllWindows()


img = cv.imread('bank_card.jpeg')
b, g, r = cv.split(img)
print(b)
cv_show('r', b)
img = cv.resize(img, None, fx=0.5, fy=0.5)
img = cv.bitwise_and(img, img)
cv_show('img', img)

# img_pyr = cv.pyrMeanShiftFiltering(img, 10, 10)
# cv_show('pyr', img_pyr)

img = cv.GaussianBlur(img, (5, 5), 0)
img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# cv_show('gray', img_gray)
# img_thresh = cv.threshold(img_gray, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
# cv_show('threshold', img_thresh)
img_canny = cv.Canny(img_gray, 60, 100)
cv_show('img_canny', img_canny)
