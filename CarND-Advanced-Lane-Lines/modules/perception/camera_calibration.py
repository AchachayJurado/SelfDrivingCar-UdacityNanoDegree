import numpy as np
import cv2
import glob
import os
import image_util
import pickle

# -------------------(Horizontal, Vertical)
chess_board_matrix = (9, 6)

objp = np.zeros((chess_board_matrix[0]*chess_board_matrix[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:chess_board_matrix[0],
                       0:chess_board_matrix[1]].T.reshape(-1, 2)


def CameraCalibration(path):
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane.

    imgs = image_util.loadImagesRGB(path)
    for img in imgs:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(
            gray, chess_board_matrix, None)

        # If found, add object points, image points
        if ret == True:
            objpoints.append(objp)
            imgpoints.append(corners)

        # Do camera calibration given object points and image points
        img_size = (img.shape[1], img.shape[0])
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(
        objpoints, imgpoints, img_size, None, None)
    return ret, mtx, dist, rvecs, tvecs


def cachedCameraCalibration(path):
    pickle_file = path + "/calibration_pickle.p"
    print(pickle_file)
    if os.path.isfile(pickle_file):
        print("pickle file exists.")
        with open(pickle_file, "rb") as f:
            dist_pickle = pickle.load(f)
        return dist_pickle["ret"], dist_pickle["mtx"],  dist_pickle["dist"], dist_pickle["rvecs"], dist_pickle["tvecs"]
    else:
        print("pickle file does not exist.")
        ret, mtx, dist, rvecs, tvecs = CameraCalibration(path)
        # Save the camera calibration result to be used later
        dist_pickle = {}
        dist_pickle["ret"] = dist
        dist_pickle["mtx"] = mtx
        dist_pickle["dist"] = dist
        dist_pickle["rvecs"] = dist
        dist_pickle["tvecs"] = dist
        with open(pickle_file, "wb") as f:
            pickle.dump(dist_pickle, f)
        return ret, mtx, dist, rvecs, tvecs
