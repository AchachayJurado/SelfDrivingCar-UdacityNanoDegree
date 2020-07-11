import numpy as np
import cv2
import matplotlib.pyplot as plt

from perception.camera_calibration import *
from perception.undistorter import *
from perception.tresholder import *
from perception.warper import *
from perception.lane_fitter import *


def LaneFinder():
    camera = GetCalibratedCamera()
    warper = Warper()
    images = glob.glob("test_images/*.jpg")

    f, axs = plt.subplots(len(images), 1, figsize=(20, 50))
    f.tight_layout()
    for idx, filename in enumerate(sorted(images)):
        image = read_image(filename)
        undistorted = undistort_image(image, camera)
        edges, _ = edge_finder(undistorted)
        warped = warp_image(warper, edges)

        lane_fitting = LaneFitter(image.shape[1], image.shape[0])
        vis_lanes = lane_fitting.fit_polynomial(warped)

        # Curvature
        left_cr, right_cr = lane_fitting.get_curvature()
        pos = lane_fitting.get_vehicle_position()

        # Concatenate
        vis_edges = np.dstack((edges, edges, edges))
        vis_edges = vis_edges * np.max(undistorted)
        vis = np.concatenate((undistorted, vis_edges, vis_lanes), axis=1)

        # Display Comparison
        axs[idx].imshow(vis)
        axs[idx].axis("off")

        # Save
        save_image(vis, filename, "lane_fitting_")

    plt.show()
