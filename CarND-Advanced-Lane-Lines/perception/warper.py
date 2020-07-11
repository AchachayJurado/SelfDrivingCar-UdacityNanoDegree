
import cv2
import numpy as np


def warp_image(warper, binary):
    warped = warper.warp(binary)
    return warped


class Warper:
    def __init__(self, img_size=(1280, 720)):
        self.src = np.float32(
            [[(img_size[0] / 2) - 62, img_size[1] / 2 + 100],
             [((img_size[0] / 6) - 10), img_size[1]],
             [(img_size[0] * 5 / 6) + 60, img_size[1]],
             [(img_size[0] / 2 + 62), img_size[1] / 2 + 100]])

        self.dst = np.float32(
            [[(img_size[0] / 4), 0],
             [(img_size[0] / 4), img_size[1]],
             [(img_size[0] * 3 / 4), img_size[1]],
             [(img_size[0] * 3 / 4), 0]])

        self.M = cv2.getPerspectiveTransform(self.src, self.dst)
        self.Minv = cv2.getPerspectiveTransform(self.dst, self.src)

    def warp(self, image):
        img_size = (image.shape[1], image.shape[0])
        return cv2.warpPerspective(image, self.M, img_size, flags=cv2.INTER_LINEAR)

    def unwarp(self, image):
        img_size = (image.shape[1], image.shape[0])
        return cv2.warpPerspective(image, self.Minv, img_size, flags=cv2.INTER_LINEAR)

    def draw_src(self, image):
        cv2.polylines(image, [np.int32(self.src)],
                      1, (0, 255, 255), thickness=8)

    def draw_dst(self, image):
        cv2.polylines(image, [np.int32(self.dst)],
                      1, (0, 255, 255), thickness=8)
