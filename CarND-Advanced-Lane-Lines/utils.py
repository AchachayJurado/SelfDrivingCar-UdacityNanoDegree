import os
import glob
import cv2
import numpy as np
import matplotlib.pyplot as plt

from perception.undistorter import *
from perception.camera_calibration import *
from perception.tresholder import *
from perception.pespective_transformer import *
from perception.lane_finder import *

TEST_IMAGES = glob.glob("test_images/*.jpg")


def RunPipelineForImage():
    camera = GetCalibratedCamera()
    warper = Warper()

    f, axs = plt.subplots(len(TEST_IMAGES), 1, figsize=(20, 50))
    f.tight_layout()
    for idx, filename in enumerate(sorted(TEST_IMAGES)):
        image = read_image(filename)
        undistorted = undistort_image(image, camera)
        edges, _ = edge_finder(undistorted)
        warped = warp_image(warper, edges)

        lane_fitting = LaneFitter(image.shape[1], image.shape[0])
        vis_lanes = lane_fitting.fit_polynomial(warped)

        # Curvature
        left_cr, right_cr = lane_fitting.get_curvature()
        offset_kpi = abs(lane_fitting.get_vehicle_position())

        # Car Offset to the center line
        pts_y, left_fitx, right_fitx = lane_fitting.get_fitpoints()

        warp_zero = np.zeros_like(warped).astype(np.uint8)
        color_warp = np.dstack((warp_zero, warp_zero, warp_zero))

        # Recast the x and y points into usable format for cv2.fillPoly()
        pts_left = np.array([np.transpose(np.vstack([left_fitx, pts_y]))])
        pts_right = np.array(
            [np.flipud(np.transpose(np.vstack([right_fitx, pts_y])))])
        pts = np.hstack((pts_left, pts_right))

        # Draw the lane onto the warped blank image
        cv2.fillPoly(color_warp, np.int_([pts]), (0, 255, 0))

        # Warp the blank back to original image space using inverse perspective matrix (Minv)
        overlay = warper.unwarp(color_warp)

        # Combine the result with the original image
        vis_process = cv2.addWeighted(undistorted, 1, overlay, 0.3, 0)

        curvature = 0.5*(left_cr/1000 + right_cr/1000)

        cr_text = "Radius of Curvature:  " + '{:6.2f}km'.format(
            curvature)
        pos_text = "Distance from Center: " + '{:6.2f}cm'.format(
            offset_kpi*100)

        def put_text(image, text, color=(0, 0, 255), ypos=100):
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, text, (430, ypos),
                        font, 1, color, 2, cv2.LINE_AA)

        put_text(vis_process, cr_text, ypos=660)
        put_text(vis_process, pos_text, ypos=700)

        # Concatenate
        vis_edges = np.dstack((edges, edges, edges))
        vis_edges = vis_edges * np.max(undistorted)
        vis_a = np.concatenate((undistorted, vis_edges), axis=1)
        vis_b = np.concatenate((vis_lanes, vis_process), axis=1)
        vis = np.concatenate((vis_a, vis_b), axis=0)

        # Display Comparison
        axs[idx].imshow(vis_process)
        axs[idx].axis("off")

        # Save
        # save_image(vis, filename, "pipeline_process_")
        save_image(vis_process, filename, "pipeline_")

    plt.show()
