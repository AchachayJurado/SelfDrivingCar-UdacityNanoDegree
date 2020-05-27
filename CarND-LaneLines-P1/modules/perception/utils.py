import os
import cv2
import numpy as np

from plot_images import *


def ProcessImage(original_image, xsize, ysize, return_process):
    # 1. Apply grayscale transform to the image
    gray_image = cv2.cvtColor(original_image, cv2.COLOR_RGB2GRAY)

    # 2. Blur/Smooth the image
    # Gaussian Filter parameters
    kernel_width = 5  # should be odd and positive
    kernel_height = 5  # should be odd and positive
    x_std_dev = 0

    blur_image = cv2.GaussianBlur(
        gray_image, (kernel_width, kernel_height), x_std_dev)

    # 3. Find edges in the images
    # Canny Feature Detection
    min_val = 50
    max_val = 150
    intensity_gradient = [min_val, max_val]

    canny_image = cv2.Canny(
        blur_image, intensity_gradient[0], intensity_gradient[1])

    # 4. Find the region of interest
    # Based on the image size and delta values given
    delta_x = 45
    delta_y = 55
    delta_bottom = 60

    region_of_interest = RegionOfInterest(
        canny_image, xsize, ysize, delta_x, delta_y, delta_bottom)

    # 5. Apply Hough Line Transform for lines
    # Input image should be a binary image
    roh = 2               # pixels accuracy
    theta = np.pi / 180   # radians accuracy
    threshold = 50        # minimum voter to be considered as a line
    # --------------------- num of votes depends on num of points in line, SO:
    # --------------------- it represents the minimin line that should be detected
    min_line_len = 120
    max_line_gap = 160

    # lines_in_image = HoughLines(
    #     region_of_interest, roh, theta, threshold, min_line_len, max_line_gap)
    lines_in_image = improved_hough_lines(
        region_of_interest, roh, theta, threshold, min_line_len, max_line_gap)
    # lines = fhough_lines(
    # region_of_interest, roh, theta, threshold, min_line_len, max_line_gap)

    # lines_in_image = imgmitlines(region_of_interest, lines)

    # 6.Alpha blend the lines in image to the original image
    alpha = 0.8  # weight of the first array elements  (original_image)
    beta = 1.    # weight of the second array elements (image only with lines)
    gamma = 0.   # scalar added to each sum

    ego_lanes_image = cv2.addWeighted(
        original_image, alpha, lines_in_image, beta, gamma)

    if return_process:
        # Return output images for steps 1 to 6
        return gray_image, blur_image, canny_image, region_of_interest, lines_in_image, ego_lanes_image
    else:
        return ego_lanes_image


def RegionOfInterest(img, xsize, ysize, delta_x, delta_y, delta_bottom):
    # Define a triangle/trapezoid to represent the region of interest
    # HINT: The origin (x=0, y=0) is in the upper left in image processing

    # 1. Define vertices by four points
    x_middle = xsize / 2
    y_middle = ysize / 2

    left_bottom = (delta_bottom, ysize)
    left_top = (x_middle - delta_x, y_middle + delta_y)
    right_bottom = (xsize - delta_bottom, ysize)
    right_top = (x_middle + delta_x, y_middle + delta_y)

    vertices = np.array(
        [[left_bottom, left_top, right_top, right_bottom]], dtype=np.int32)

    # 2 Define a blank mask to start with
    mask = np.zeros_like(img)

    # 3. Define channel color to fill the mask with
    if len(img.shape) < 2:
        channel_count = img.shape[2]
        ignore_mask_color = (255,) * channel_count
    else:
        ignore_mask_color = 255

    # 4. Fill pixels inside the polygon defined by the vertices with the fill color
    cv2.fillPoly(mask, vertices, ignore_mask_color)

    # 5. Return the image only where mask pixels are nonzero
    masked_image = cv2.bitwise_and(img, mask)

    return masked_image


def DrawLines(img, lines, color, thickness=8):
    for line in lines:
        cv2.line(img, (line[0][0], line[0][1]),
                 (line[0][2], line[0][3]), color, thickness)


def DrawLine(img, lines, color, thickness=8):
    for line in lines:
        cv2.line(img, (line[0], line[1]), (line[2], line[3]), color, thickness)


def HoughLines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)
    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    line_color = [245, 0, 245]  # purple :)
    DrawLines(line_img, lines, line_color)
    return line_img
# ===========================================================================================
#     ----   Improving Hough Lines   ------
# ===========================================================================================


def divide_lines(img, lines):
    x_middle = img.shape[1] / 3

    # Left Lines Collection
    all_left_lines = []
    left_lines = []

    # Right Lines Collection
    all_right_lines = []
    right_lines = []

    for line in lines:
        if abs(line[0][0] - line[0][2]) > 2:
            k = (line[0][3] - line[0][1]) * 1.0 / (line[0][2] - line[0][0])
            if line[0][0] < x_middle and k < -0.5:
                all_left_lines.append(line[0])
            elif line[0][2] > x_middle and k > 0.5:
                all_right_lines.append(line[0])
        else:
            all_left_lines = left_lines

    all_left_lines.sort(key=lambda x: x[0])
    all_right_lines.sort(key=lambda x: x[0])

    for line in all_left_lines:
        if len(left_lines) != 0:
            if line[0] > left_lines[-1][2] and line[1] < left_lines[-1][3]:
                left_lines.append(
                    [left_lines[-1][2], left_lines[-1][3], line[0], line[1]])
                left_lines.append([line[0], line[1], line[2], line[3]])
        else:
            left_lines.append([line[0], line[1], line[2], line[3]])

    for line in all_right_lines:
        if len(right_lines) != 0:
            if line[0] > right_lines[-1][2] and line[1] > right_lines[-1][3]:
                right_lines.append(
                    [right_lines[-1][2], right_lines[-1][3], line[0], line[1]])
                right_lines.append([line[0], line[1], line[2], line[3]])
        else:
            right_lines.append([line[0], line[1], line[2], line[3]])

    return left_lines, right_lines


def improved_lines(left_lines, right_lines, shape):
    ysize = shape[0]

    left_bottom = [left_lines[0][0], left_lines[0][1]]
    left_top = [left_lines[-1][2], left_lines[-1][3]]
    right_top = [right_lines[0][0], right_lines[0][1]]
    right_bottom = [right_lines[-1][2], right_lines[-1][3]]

    k_left = (left_top[1] - left_bottom[1]) * \
        1.0 / (left_top[0] - left_bottom[0])
    k_right = (right_top[1] - right_bottom[1]) * \
        1.0 / (right_top[0] - right_bottom[0])

    left_bottom2 = [
        int(left_bottom[0] - (left_bottom[1] - ysize) / k_left), ysize]
    left_top2 = [int(left_top[0] - (left_top[1] -
                                    (ysize / 2 + 50)) / k_left), int(ysize / 2 + 50)]
    right_bottom2 = [
        int(right_bottom[0] - (right_bottom[1] - ysize) / k_right), ysize]
    right_top2 = [int(right_top[0] - (right_top[1] -
                                      (ysize / 2 + 50)) / k_right), int(ysize / 2 + 50)]

    left_lines.append([left_bottom[0], left_bottom[1],
                       left_bottom2[0], left_bottom2[1]])
    left_lines.append([left_top[0], left_top[1], left_top2[0], left_top2[1]])
    right_lines.append([right_bottom[0], right_bottom[1],
                        right_bottom2[0], right_bottom2[1]])
    right_lines.append([right_top[0], right_top[1],
                        right_top2[0], right_top2[1]])

    return left_lines, right_lines


def improved_hough_lines(img, rho, theta, threshold, min_line_len, max_line_gap):
    lines = cv2.HoughLinesP(img, rho, theta, threshold, np.array([]), minLineLength=min_line_len,
                            maxLineGap=max_line_gap)

    left_lines, right_lines = divide_lines(img, lines)
    try:
        left_lines, right_lines = improved_lines(
            left_lines, right_lines, img.shape)
    except IndexError:
        left_lines = left_lines

    left_line_color = [255, 0, 255]
    right_line_color = [0, 245, 245]

    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    DrawLine(line_img, left_lines, left_line_color)
    DrawLine(line_img, right_lines, right_line_color)

    return line_img

################################################################################################
################################################################################################


def slope(x1, y1, x2, y2):
    return (y1 - y2) / (x1 - x2)


def separate_lines(lines):
    right = []
    left = []

    print(lines[:, 0])
    for x1, y1, x2, y2 in lines[:, 0]:
        print(x1, y1, x2, y2)
        m = slope(x1, y1, x2, y2)
        if m >= 0:
            right.append([x1, y1, x2, y2, m])
        else:
            left.append([x1, y1, x2, y2, m])
    return right, left


def reject_outliers(data, cutoff, threshold=0.08):
    data = np.array(data)
    data = data[(data[:, 4] >= cutoff[0]) & (data[:, 4] <= cutoff[1])]
    m = np.mean(data[:, 4], axis=0)
    return data[(data[:, 4] <= m+threshold) & (data[:, 4] >= m-threshold)]


def lines_linreg(lines_array):
    print(lines_array.shape)
    x = np.reshape(lines_array[:, :, [0, 2]], (1, len(lines_array) * 2))[0]
    print(len(x))
    y = np.reshape(lines_array[:, :, [1, 3]], (1, len(lines_array) * 2))[0]
    A = np.vstack([x, np.ones(len(x))]).T
    m, c = np.linalg.lstsq(A, y)[0]
    x = np.array(x)
    print(len(y))
    y = np.array(x * m + c)
    return x, y, m, c


def extend_point(x1, y1, x2, y2, length):
    line_len = np.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    x = x2 + (x2 - x1) / line_len * length
    y = y2 + (y2 - y1) / line_len * length
    return x, y


def imgmitlines(img, lines):
    right_lines, left_lines = separate_lines(lines)
    if right_lines and left_lines:
        right = reject_outliers(right_lines,  cutoff=(0.45, 0.75))
        left = reject_outliers(left_lines, cutoff=(-0.85, -0.6))
    # This variable represents the top-most point in the image where we can reasonable draw a line to.
    x, y, m, c = lines_linreg(lines)
    # # Calculate the top point using the slopes and intercepts we got from linear regression.
    min_y = np.min(y)
    # # Repeat this process to find the bottom left point
    top_point = np.array([(min_y - c) / m, min_y], dtype=int)
    max_y = np.max(y)
    bot_point = np.array([(max_y - c) / m, max_y], dtype=int)
    x1e, y1e = extend_point(
        bot_point[0], bot_point[1], top_point[0], top_point[1], -1000)  # bottom point
    x2e, y2e = extend_point(
        bot_point[0], bot_point[1], top_point[0], top_point[1],  1000)  # top point

    line = np.array([[x1e, y1e, x2e, y2e]])
    line_p = np.array([line], dtype=np.int32)

    left_line_color = [255, 0, 255]
    right_line_color = [0, 245, 245]

    line_img = np.zeros((img.shape[0], img.shape[1], 3), dtype=np.uint8)
    # DrawLine(line_img, left_lines, left_line_color)
    # DrawLine(line_img, right_lines, right_line_color)
    # DrawLine(line_img, line_p, right_line_color)
    draw_lines(line_img, lines, thickness=3)
    draw_lines(line_img, right, thickness=3)
    return line_img


def fhough_lines(image, rho, theta, threshold, min_line_len, max_line_gap):
    rho = 2
    theta = np.pi/180
    threshold = 50
    min_line_len = 120
    max_line_gap = 150
    lines = cv2.HoughLinesP(image, rho, theta, threshold, np.array(
        []), minLineLength=min_line_len, maxLineGap=max_line_gap)
    return lines


def draw_lines(image, lines, color=[255, 0, 0], thickness=2):
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(image, (x1, y1), (x2, y2), color, thickness)
