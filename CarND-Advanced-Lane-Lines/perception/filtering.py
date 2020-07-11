import os
import cv2
import numpy as np
import matplotlib.pyplot as plt

from .save import save_image


class HLSFilter:
    def __init__(self):
        pass

    def filter_s(self, img, thresh=(150, 255)):
        hls = cv2.cvtColor(img, cv2.COLOR_RGB2HLS)
        s_channel = hls[:, :, 2]
        binary_output = np.zeros_like(s_channel)
        binary_output[(s_channel > thresh[0]) & (s_channel <= thresh[1])] = 1
        return binary_output, s_channel


class SobelFilter:
    def __init__(self, kernel_size):
        self.kernel_size = kernel_size

    def filter_x(self, gray, threshold=(50, 255)):
        sobel = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=self.kernel_size)
        img_abs = np.absolute(sobel)
        scaled = np.uint8(255 * img_abs / np.max(img_abs))
        binary_output = np.zeros_like(scaled)
        binary_output[(scaled > threshold[0]) & (scaled <= threshold[1])] = 1
        return binary_output, scaled, sobel

    def filter_y(self, gray, threshold=(50, 255)):
        sobel = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=self.kernel_size)
        img_abs = np.absolute(sobel)
        scaled = np.uint8(255 * img_abs / np.max(img_abs))
        binary_output = np.zeros_like(scaled)
        binary_output[(scaled > threshold[0]) & (scaled <= threshold[1])] = 1
        return binary_output, scaled, sobel

    def filter_mag(self, sx, sy, threshold=(50, 255)):
        sobel = np.sqrt(sx ** 2 + sy ** 2)
        img_abs = np.absolute(sobel)
        scaled = np.uint8(255 * img_abs / np.max(img_abs))
        binary_output = np.zeros_like(scaled)
        binary_output[(scaled > threshold[0]) & (scaled <= threshold[1])] = 1
        return binary_output, scaled, sobel

    def filter_dir(self, sx, sy, threshold=(60, 20)):
        theta = threshold[0] * np.pi / 180.0
        delta = threshold[1] * np.pi / 180.0
        rad_threshold = [theta-delta, theta+delta]
        absx = np.absolute(sx)
        absy = np.absolute(sy)
        sobel = np.arctan2(absy, absx)
        binary = np.zeros_like(sobel)
        binary[(sobel >= rad_threshold[0]) & (sobel <= rad_threshold[1])] = 1

        return binary, sobel
