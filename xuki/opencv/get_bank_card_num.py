# @Time : 2020/9/8 16:00
# @Author : Xuki
# @File : get_bank_card_num.py
# @Annotation :

import cv2
import numpy as np

# dat = np.random.randint(1, 20, (3, 3))
# dat = dat[..., None]
# print(dat)
# print(dat.shape)
# exit(0)


def cv_show(name, img):
    cv2.imshow(name, img)
    cv2.waitKey(0)
    # cv2.destroyAllWindows()


img = cv2.imread('bank_card.jpg')
img_original = img.copy()
img = cv2.pyrMeanShiftFiltering(img, sp=10, sr=10)
cv_show('img', img)
h, w, _ = img.shape
img = img.reshape((h * w, 3))
img = np.float32(img)
K = 5
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 10, 0.5)
retval, bestLabels, centers = cv2.kmeans(img, K, None, criteria=criteria, attempts=10, flags=cv2.KMEANS_RANDOM_CENTERS)

mask_value = bestLabels[0][0]
mask = np.full(img_original.shape, 255, dtype=np.uint8)
bestLabels_shaped = bestLabels.reshape((h, w))
mask[bestLabels_shaped == mask_value] = 0

se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
cv2.erode(mask, se, mask)

mask = cv2.GaussianBlur(mask, (5, 5), 0)
cv_show('mask', mask)

exit(0)

original = img.copy()
img = cv2.pyrMeanShiftFiltering(img, sp=10, sr=10)
cv_show('pyrMeanShiftFiltering', img)

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv_show('GRAY', img)

img = cv2.threshold(img, 0, 255,
                    cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
cv_show('thresh', img)

cnts = cv2.findContours(img, cv2.RETR_EXTERNAL,
                        cv2.CHAIN_APPROX_SIMPLE)[0]
print(len(cnts))
cv2.drawContours(original, cnts, -1, (255, 0, 0), 3)
cv_show('thresh_Contours', original)
