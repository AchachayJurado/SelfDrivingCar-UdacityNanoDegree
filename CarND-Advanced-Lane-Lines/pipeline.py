# from perception.lane_tracker import LaneLinesTracker
from utils import *

from perception.undistorter import *
from perception.camera_calibration import *
from perception.treshold import *


def pipeline():
    # --------
    # 1. For a given set of chessboard images, apply the camera calibration matrix and distortion coefficients.
    # --------
    # CalibrateCamera()
    # --------
    # 2. Compute distortion correction to raw images.
    # --------
    # RemoveDistortion()

    # --------
    # 3. Set a treshold for a binary image to use color transforms, gradients, etc.
    # --------
    DetectEdges()

    # --------
    # 4. Apply a perspective transform to rectify binary image.
    # --------
    # PerspectiveTransform()

    # --------
    # 5. Fit the lane by:
    #    - Finding the lane boundary by detecting lane pixels.
    #    - Determining the curvature of the lane and vehicle position with respect to center.
    # --------
    # FitLaneBoundaries()

    # --------
    # 6. Warp the detected lane boundaries back onto the original image.
    # --------
    # RunPipelineForImage()

    # --------
    # 8. Output a collection of images as a visual display of the lane boundaries
    #    and numerical estimation of lane curvature and vehicle position.
    # --------
    # RunPipelineForVideo(subclip_seconds=0.5)


if __name__ == "__main__":
    pipeline()
