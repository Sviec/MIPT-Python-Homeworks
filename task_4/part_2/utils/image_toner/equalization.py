import cv2


def histogram_equalization(img, save_as: str):
    src = cv2.imread(img, cv2.IMREAD_GRAYSCALE)
    src = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    cv2.imwrite(cv2.equalizeHist(src), save_as)
