import pickle
import cv2
import camera_calibration
import os

# the camera_cal images are expected relatively to THIS python file
CAMERA_CAL_DIR = os.path.dirname(os.path.abspath(__file__))+"/camera_cal"


class Undistorter:

    def __init__(self):
        self.ret, self.mtx, self.dist, self.rvecs, self.tvecs = camera_calibration.cachedCalibrateCameraFromDir(
            CAMERA_CAL_DIR)

    def undistort(self, img):
        return cv2.undistort(img, self.mtx, self.dist)
