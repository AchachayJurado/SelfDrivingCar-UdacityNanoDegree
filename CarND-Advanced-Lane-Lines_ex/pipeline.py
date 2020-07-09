import perspective_trafo as pt
import undistorter as ud
import lanefinder as lf
import cv2
import curvature as cv
import threshold as th
import numpy as np


class Pipeline:
    def __init__(self):
        self.undistorter = ud.Undistorter()
        self.perspectiveTrafo = pt.PerspectiveTrafo(img_size=(1280, 720))
        self.lanefinder = lf.LaneFinder()

    def process(self, img):
        undistorted_img = self.undistorter.undistort(img)

        # Choose a Sobel kernel size
        ksize = 3  # Choose a larger odd number to smooth gradient measurements

        # Apply each of the thresholding functions
        gradx = th.abs_sobel_thresh(
            undistorted_img, orient='x', sobel_kernel=ksize, thresh=(20, 100))
        grady = th.abs_sobel_thresh(
            undistorted_img, orient='y', sobel_kernel=ksize, thresh=(20, 100))
        mag_binary = th.mag_thresh(
            undistorted_img, sobel_kernel=ksize, mag_thresh=(30, 170))
        dir_binary = th.dir_threshold(
            undistorted_img, sobel_kernel=ksize, thresh=(0, np.pi/2))
        s_binary = th.hls_select(undistorted_img, thresh=(90, 255))

        combined = np.zeros_like(dir_binary)
        combined[((gradx == 1) & (grady == 1)) | (
            (mag_binary == 1) & (dir_binary == 1)) | (s_binary == 1)] = 1

        #combined2 = np.array(combined*255, dtype=np.uint8)
        #combined2 = img = cv2.cvtColor(combined2 ,cv2.COLOR_GRAY2RGB)

        # perspective transformation
        img = self.perspectiveTrafo.warp(combined)

        # find the lanes
        res = self.lanefinder.findLanes(img)

        # draw the frames
        (out, l, r, lcr, rcr) = res
        laneOverlay = self.lanefinder.draw(out, l, r, self.perspectiveTrafo)
        img = cv2.addWeighted(undistorted_img, 1, laneOverlay, 0.3, 0)
        (lcurve, rcurve) = cv.curvature(lcr, rcr)
        curvature = 0.5*(lcurve/1000 + rcurve/1000)
        cv2.putText(img, "Radius of Curvature:  " + '{:6.2f}km'.format(
            curvature), (430, 660), cv2.FONT_HERSHEY_SIMPLEX, 1.0, [0, 0, 255], 2, cv2.LINE_AA)
        (ll, lr, caroff) = cv.lanepos(l, r)
        cv2.putText(img, "Distance from Center: " + '{:6.2f}cm'.format(
            caroff*100), (430, 700), cv2.FONT_HERSHEY_SIMPLEX, 1.0, [0, 0, 255], 2, cv2.LINE_AA)

        return img
