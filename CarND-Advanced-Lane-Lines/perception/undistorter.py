import pickle
import cv2
import os
import matplotlib.pyplot as plt
import numpy as np
import glob

from .save import save_image
from perception.camera_calibration import GetCalibratedCamera


TEST_IMAGES = glob.glob("test_images/*.jpg")
images_directory = "test_images/"

# To visualize easier the distortion correction, it is easier to process chessboard images
# TEST_IMAGES = [
#     "camera_cal/calibration1.jpg",
#     "camera_cal/calibration2.jpg",
#     "camera_cal/calibration3.jpg",
#     "camera_cal/calibration4.jpg",
# ]


def CalibrateCamera():
    camera = GetCalibratedCamera()
    camera.display_calibration()


def undistort_image(image, camera):
    undistorted = camera.undistort(image)
    return undistorted


def read_image(filename):
    image = cv2.imread(filename)
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return rgb_image


def RemoveDistortion():
    # As 1st step the camera calibration needs to take place
    camera = GetCalibratedCamera()

    # Correct distortion save and display results
    f, axs = plt.subplots(len(TEST_IMAGES), 1, figsize=(10, 10))
    f.tight_layout()
    axs[0].set_title("Original vs Undistorted Images", fontsize=11)
    image_number = 1
    for idx, filename in enumerate(sorted(TEST_IMAGES)):
        image = read_image(filename)                   # Original Image
        undistorted = undistort_image(image, camera)   # Undistorted Image
        # Concatenate
        vis = np.concatenate((image, undistorted), axis=1)
        # Display Comparison
        axs[idx].imshow(vis)
        axs[idx].axis("off")
        # Save Single Undistorted Image
        save_image(vis, filename, "distortion_correction_")
    out_filename = os.path.join("output_images", "distortion_correction.png")
    plt.savefig(out_filename)
    plt.show()
