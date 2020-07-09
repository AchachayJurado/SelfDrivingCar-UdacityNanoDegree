import os
import math
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

from .cache import Cache
from .save import save_image


class CameraModel:
    """Computes objpoints,imgpoints pair based on chessboard images for calibration"""

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3d points in real world space.
    imgpoints = []  # 2d points in image plane.
    images = []  # images from which these points where computed.

    # Calibration
    cal_w = None
    cal_h = None
    mtx = None
    dist = None

    def __init__(self):
        self.nx = 9
        self.ny = 6
        self.target_images = glob.glob("camera_cal/calibration*.jpg")

        # cache
        self.cache = Cache("calibration.p")

    def save(self):
        data = dict()
        data["objpoints"] = self.objpoints
        data["imgpoints"] = self.imgpoints
        data["images"] = self.images
        self.cache.save(data)

    def load(self):
        if self.cache.exists():
            data = self.cache.load()
            self.objpoints = data["objpoints"]
            self.imgpoints = data["imgpoints"]
            self.images = data["images"]
            return True
        return False

    def calibrate(self):
        if self.load():
            print("Using cached calibration data ...")
            return
        print("Running calibration on %d images ..." % len(self.target_images))

        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((self.nx * self.ny, 3), np.float32)
        objp[:, :2] = np.mgrid[0: self.nx, 0: self.ny].T.reshape(-1, 2)

        # Step through the list and search for chessboard corners
        for fname in self.target_images:
            self.calibrate_single(fname, objp)

        # Update cache
        self.save()

    def calibrate_single(self, fname, objp):
        # Log.info("file: " + fname)
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(
            gray, (self.nx, self.ny), None)

        # If found, save object points, image points
        if ret == True:
            self.images.append(fname)
            self.objpoints.append(objp)
            self.imgpoints.append(corners)
        else:
            print("cv2.findChessboardCorners was not able to process file: %s" % fname)

    def display_calibration(self):
        n_images = len(self.images)
        n_columns = 4
        n_rows = int(math.ceil(n_images / 4))

        f, axs = plt.subplots(n_rows, n_columns, figsize=(40, 30))
        f.tight_layout()

        # Draw and display the corners
        for idx, fname in enumerate(self.images):
            # draw on image
            img = cv2.imread(fname)
            chessboard = cv2.drawChessboardCorners(
                img, (self.nx, self.ny), self.imgpoints[idx], True
            )

            # save to file
            save_image(chessboard, fname, "calibrated_")

            col = int(idx % n_columns)
            row = int(math.floor(idx / n_columns))-1
            axs[row, col].imshow(chessboard)
            axs[row, col].axis("off")

        # Make sure to clean empty placeholders
        for idx in range(n_images, n_rows * n_columns):
            col = idx % n_columns
            row = math.floor(idx / n_columns)
            axs[row, col].axis("off")

        out_fname = os.path.join("output_images", "calibration.png")
        plt.savefig(out_fname)
        print(
            "Found corners and calibration output saved in output_images/calibration.png")

        plt.show()

    def get_3d_to_2d_points(self):
        return self.objpoints, self.imgpoints

    def get_calibration(self, w, h):
        # Use cached
        if w == self.cal_w and h == self.cal_h:
            return self.mtx, self.dist

        # Compute
        [_, self.mtx, self.dist, _, _] = cv2.calibrateCamera(
            self.objpoints, self.imgpoints, (w, h), None, None
        )

        self.cal_w = w
        self.cal_h = h

        return self.mtx, self.dist

    def undistort(self, img):
        w = img.shape[1]
        h = img.shape[0]
        [mtx, dist] = self.get_calibration(w, h)
        undistorted = cv2.undistort(img, mtx, dist, None, mtx)
        return undistorted


def GetCalibratedCamera():
    camera = CameraModel()
    camera.calibrate()
    return camera


class WarpMachine:
    h = 720
    left = 210
    right = 1110
    top = 460
    top_left = 580
    top_right = 705
    dst_l = 320
    dst_r = 960

    def __init__(self):
        h = self.h
        l = self.left
        r = self.right
        t = self.top
        tl = self.top_left
        tr = self.top_right
        dl = self.dst_l
        dr = self.dst_r

        self.src = np.float32([[l, h], [tl, t], [tr, t], [r, h]])
        self.dst = np.float32([[dl, h], [dl, 0], [dr, 0], [dr, h]])
        self.M = cv2.getPerspectiveTransform(self.src, self.dst)
        self.Minv = cv2.getPerspectiveTransform(self.dst, self.src)

    def warp(self, image):
        img_size = (image.shape[1], image.shape[0])
        return cv2.warpPerspective(image, self.M, img_size, flags=cv2.INTER_LINEAR)

    def unwarp(self, image):
        img_size = (image.shape[1], image.shape[0])
        return cv2.warpPerspective(image, self.Minv, img_size, flags=cv2.INTER_LINEAR)

    def draw_src(self, image):
        cv2.polylines(image, [np.int32(self.src)], 1, (255, 0, 0), thickness=5)

    def draw_dst(self, image):
        cv2.polylines(image, [np.int32(self.dst)], 1, (255, 0, 0), thickness=5)
