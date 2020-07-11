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
    for idx, fname in enumerate(sorted(images)):
        image = read_image(fname)
        undistorted = undistort_image(image, camera)
        edges, _ = edge_finder(undistorted)
        warped = warp_image(warper, edges)

        lane_fitting = LaneFitter(image.shape[1], image.shape[0])
        vis_lanes = lane_fitting.fit_polynomial(warped)

        # Curvature
        left_cr, right_cr = lane_fitting.get_curvature()
        pos = lane_fitting.get_vehicle_position()

        # Drawing
        pos_str = "Left" if pos < 0 else "Right"
        # print(left_cr)
        # print(right_cr)
        # crl_text = "Radius of curvature (left) = %d m" % left_cr
        # crr_text = "Radius of curvature (right) = %d m" % right_cr
        # cr_text = "Radius of curvature (avg) = %d m" % ((left_cr + right_cr) / 2)
        # pos_text = "Vehicle is %.1f m %s from the lane center" % (np.abs(pos), pos_str)

        def put_text(image, text, color=(0, 255, 255), ypos=100):
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, text, (350, ypos),
                        font, 1, color, 2, cv2.LINE_AA)

        # put_text(vis_lanes, crl_text, ypos=50)
        # put_text(vis_lanes, crr_text, ypos=100)
        # put_text(vis_lanes, cr_text, ypos=150)
        # put_text(vis_lanes, pos_text, ypos=200)

        # Concatenate
        vis_edges = np.dstack((edges, edges, edges))
        vis_edges = vis_edges * np.max(undistorted)
        vis = np.concatenate((undistorted, vis_edges, vis_lanes), axis=1)

        # Display Comparison
        axs[idx].imshow(vis)
        axs[idx].axis("off")

        # Save
        save_image(vis, fname, "lane_fitting_")

    plt.show()
