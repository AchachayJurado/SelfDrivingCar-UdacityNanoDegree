import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

from perception.camera_calibration import GetCalibratedCamera


def CalibrateCamera():
    camera = GetCalibratedCamera()
    camera.display_calibration()
