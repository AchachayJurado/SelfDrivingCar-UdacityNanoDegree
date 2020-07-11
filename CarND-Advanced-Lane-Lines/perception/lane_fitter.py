import numpy as np
import matplotlib.pyplot as plt
import cv2


class LaneFitter(object):

    # lane size [m]
    lane_width = 3.7
    lane_depth = 30

    # lane polynomials
    left_fit = None
    right_fit = None

    def __init__(self, img_width, img_height):
        self.image_width = img_width
        self.image_height = img_height

        # y pixel where to measure curvature/position
        self.target_px = self.image_height

        # pixel to meters conversions
        self.ym_per_pix = self.lane_depth / self.image_height
        self.xm_per_pix = self.lane_width / 700

    def find_lane_pixels(self, binary_warped):
        # Take a histogram of the bottom half of the image
        # Lane lines are likely to be mostly vertical nearest to the car
        histogram = np.sum(
            binary_warped[binary_warped.shape[0] // 2:, :], axis=0)

        # Create an output image to draw on and visualize the result
        out_img = np.dstack((binary_warped, binary_warped, binary_warped))
        out_img = out_img * 255

        # Find the peak of the left and right halves of the histogram
        # These will be the starting point for the left and right lines
        midpoint = np.int(histogram.shape[0] // 2)
        leftx_base = np.argmax(histogram[:midpoint])
        rightx_base = np.argmax(histogram[midpoint:]) + midpoint

        # HYPERPARAMETERS
        # Choose the number of sliding windows
        nwindows = 9
        # Set the width of the windows +/- margin
        margin = 100
        # Set minimum number of pixels found to recenter window
        minpix = 50

        # Set height of windows - based on nwindows above and image shape
        window_height = np.int(binary_warped.shape[0] // nwindows)

        # Identify the x and y positions of all nonzero pixels in the image
        nonzero = binary_warped.nonzero()
        nonzeroy = np.array(nonzero[0])
        nonzerox = np.array(nonzero[1])

        # Current positions to be updated later for each window in nwindows
        leftx_current = leftx_base
        rightx_current = rightx_base

        # Create empty lists to receive left and right lane pixel indices
        left_lane_inds = []
        right_lane_inds = []

        # Step through the windows one by one
        for window in range(nwindows):
            # Identify window boundaries in x and y (and right and left)
            win_y_low = binary_warped.shape[0] - (window + 1) * window_height
            win_y_high = binary_warped.shape[0] - window * window_height

            win_xleft_low = leftx_current - margin
            win_xleft_high = leftx_current + margin
            win_xright_low = rightx_current - margin
            win_xright_high = rightx_current + margin

            # Draw the windows on the visualization image
            cv2.rectangle(
                out_img,
                (win_xleft_low, win_y_low),
                (win_xleft_high, win_y_high),
                (0, 255, 0),
                2,
            )
            cv2.rectangle(
                out_img,
                (win_xright_low, win_y_low),
                (win_xright_high, win_y_high),
                (0, 255, 0),
                2,
            )

            # Identify the nonzero pixels in x and y within the window ###
            non_zero_left_inds = (
                (nonzeroy >= win_y_low)
                & (nonzeroy < win_y_high)
                & (nonzerox >= win_xleft_low)
                & (nonzerox < win_xleft_high)
            ).nonzero()[0]
            non_zero_right_inds = (
                (nonzeroy >= win_y_low)
                & (nonzeroy < win_y_high)
                & (nonzerox >= win_xright_low)
                & (nonzerox < win_xright_high)
            ).nonzero()[0]

            # Append these indices to the lists
            left_lane_inds.append(non_zero_left_inds)
            right_lane_inds.append(non_zero_right_inds)

            # If you found > minpix pixels, recenter next window on their mean position
            if len(non_zero_left_inds) > minpix:
                leftx_current = np.int(np.mean(nonzerox[non_zero_left_inds]))
                if len(non_zero_right_inds) > minpix:
                    rightx_current = np.int(
                        np.mean(nonzerox[non_zero_right_inds]))

        # Concatenate the arrays of indices (previously was a list of lists of pixels)
        left_lane_inds = np.concatenate(left_lane_inds)
        right_lane_inds = np.concatenate(right_lane_inds)

        # Extract left and right line pixel positions
        leftx = nonzerox[left_lane_inds]
        lefty = nonzeroy[left_lane_inds]
        rightx = nonzerox[right_lane_inds]
        righty = nonzeroy[right_lane_inds]

        return leftx, lefty, rightx, righty, out_img

    def fit_polynomial(self, binary_warped):
        # Find our lane pixels first
        leftx, lefty, rightx, righty, out_img = self.find_lane_pixels(
            binary_warped)

        # Fit a second order polynomial to each using `np.polyfit`
        self.left_fit = np.polyfit(lefty, leftx, 2)
        self.right_fit = np.polyfit(righty, rightx, 2)

        # Visualization
        self.draw_lanes(out_img, leftx, lefty, rightx, righty)
        return out_img

    def draw_polyfit(self, image, fit):
        try:
            py = list(range(image.shape[0]))
            px = np.polyval(fit, py)
            points = (np.asarray([px, py]).T).astype(np.int32)
            cv2.polylines(image, [points], False,
                          color=(255, 255, 0), thickness=10)
        except TypeError:
            print("The function failed to fit a line!")

    def get_fitpoints(self):
        points_y = list(range(self.image_height))
        left_fitx = np.polyval(self.left_fit, points_y)
        right_fitx = np.polyval(self.right_fit, points_y)
        return points_y, left_fitx, right_fitx

    def draw_lanes(self, image, leftx, lefty, rightx, righty):
        # Colors in the left and right lane regions
        image[lefty, leftx] = [255, 0, 0]
        image[righty, rightx] = [0, 0, 255]

        # Draw fitted polynomial
        self.draw_polyfit(image, self.left_fit)
        self.draw_polyfit(image, self.right_fit)

    def get_curvature_px(self):
        """Calculates the curvature of polynomial functions in pixels."""

        # Implement the calculation of R_curve (radius of curvature)
        def compute(y, A, B):
            return (1 + (2 * A * y + B) ** 2) ** (3 / 2) / np.abs(2 * A)

        y = self.target_px
        left_curverad = compute(y, self.left_fit[0], self.left_fit[1])
        right_curverad = compute(y, self.right_fit[0], self.right_fit[1])

        print(left_curverad)
        print(right_curverad)

        return left_curverad, right_curverad

    def get_curvature(self):
        """Returns the curvature of polynomial functions in meters."""

        # Implement the calculation of R_curve (radius of curvature)
        def compute(y, A, B):
            Am = A * self.xm_per_pix / (self.ym_per_pix ** 2)
            Bm = B * self.xm_per_pix / self.ym_per_pix
            return (1 + (2 * Am * y + Bm) ** 2) ** (3 / 2) / np.abs(2 * Am)

        y = self.target_px
        left_curverad = compute(y, self.left_fit[0], self.left_fit[1])
        right_curverad = compute(y, self.right_fit[0], self.right_fit[1])

        return left_curverad, right_curverad

    def get_vehicle_position(self):
        """
        Returns vehicle distance to the lane center in meters.
        Assumes camera is exactly at the middle of the vehicle.

        Positive value: vehicle is to the right.
        Negative value: vehicle is to the left.
        """
        left = np.polyval(self.left_fit, self.target_px)
        right = np.polyval(self.right_fit, self.target_px)
        img_center = self.image_width / 2
        lane_center = (left + right) / 2

        delta = lane_center - img_center

        return -1 * delta * self.xm_per_pix
