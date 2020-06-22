import camera_calibration as run
import image_util
import sys
import os
import unittest
import cv2

sys.path.append("..")

# Input images directories
CAMERA_CAL_DIR = "camera_cal"
TEST_IMAGES_DIR = "test_images"

# Output images directory
TEST_OUT_DIR = "debug_output_images/calibration/"


class CameraCalibrationTest(unittest.TestCase):
    def setUp(self):
        if not os.path.exists(TEST_OUT_DIR):
            os.makedirs(TEST_OUT_DIR)

    def tearDown(self):
        return

    def test_01_CameraCalibration(self):
        ret, mtx, dist, rvecs, tvecs = run.cachedCameraCalibration(
            CAMERA_CAL_DIR)
        print("Run Cached Camera Calibration for images in ", CAMERA_CAL_DIR)
        print(ret)
        print(mtx)
        print(dist)

    def test_02_UndistortCalibrationImages(self):
        imgs = image_util.loadImagesRGB(CAMERA_CAL_DIR)
        ret, mtx, dist, rvecs, tvecs = run.cachedCameraCalibration(
            CAMERA_CAL_DIR)
        for i, img in enumerate(imgs):
            dimg = cv2.undistort(img, mtx, dist)
            image_util.saveBeforeAfterImages(
                img, "Original", dimg, "Undistorted", TEST_OUT_DIR+"/chess_"+str(i)+"_undistorted.png")

    def test_03_UndistortTestImages(self):
        imgs = image_util.loadImagesRGB(TEST_IMAGES_DIR)
        ret, mtx, dist, rvecs, tvecs = run.cachedCameraCalibration(
            CAMERA_CAL_DIR)
        for i, img in enumerate(imgs):
            dimg = cv2.undistort(img, mtx, dist)
            image_util.saveBeforeAfterImages(
                img, "Original", dimg, "Undistorted", TEST_OUT_DIR+"/test_image _"+str(i)+"_undistorted.png")


if __name__ == '__main__':
    unittest.main()
