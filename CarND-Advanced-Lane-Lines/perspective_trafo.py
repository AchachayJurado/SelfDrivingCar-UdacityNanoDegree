import cv2
import numpy as np
import glob


class PerspectiveTrafo:
    M = []

    DEFAULT_SRC = np.float32(
        [[120, 720],
            [550, 470],
            [730, 470],
            [1160, 720]])

    DEFAULT_DST = np.float32(
        [[200, 720],
            [200, 0],
            [1080, 0],
            [1080, 720]])

    def __init__(self, img_size=(1300, 1300)):
        src = np.float32(
            [[(img_size[0] / 2) - 62, img_size[1] / 2 + 100],
             [((img_size[0] / 6) - 10), img_size[1]],
             [(img_size[0] * 5 / 6) + 60, img_size[1]],
             [(img_size[0] / 2 + 62), img_size[1] / 2 + 100]])

        dst = np.float32(
            [[(img_size[0] / 4), 0],
             [(img_size[0] / 4), img_size[1]],
             [(img_size[0] * 3 / 4), img_size[1]],
             [(img_size[0] * 3 / 4), 0]])

        print("src")
        print(src)

        print("dst")
        print(dst)

        self.M = cv2.getPerspectiveTransform(src, dst)
        self.Minv = cv2.getPerspectiveTransform(dst, src)
        self.img_size = img_size

    def warp(self, img):
        return cv2.warpPerspective(img, self.M, self.img_size, flags=cv2.INTER_LINEAR)

    def warpInv(self, img, img_size):
        return cv2.warpPerspective(img, self.Minv, img_size, flags=cv2.INTER_LINEAR)
