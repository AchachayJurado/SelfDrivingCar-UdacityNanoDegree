# from perception.lane_tracker import LaneLinesTracker
from utils import *


def pipeline():
    # --------
    # Uncomment to run the specific steps to get output_images for each of them
    # --------

    # -- For a given set of chessboard images, apply the camera calibration matrix and distortion coefficients.
    # CalibrateCamera()

    # -- Compute distortion correction to raw images.
    # RemoveDistortion()

    # -- Set a treshold for a binary image to use color transforms, gradients, etc.
    # -- and warp the detected lane boundaries back onto the original image.
    # DetectEdges()

    # -- Apply a perspective transform to rectify binary image.
    # PerspectiveTransform()

    # -- Fit the lane by:
    #    - Finding the lane boundary by detecting lane pixels.
    #    - Determining the curvature of the lane and vehicle position with respect to center.
    # LaneFinder()

    # RunPipelineForImage()

    RunPipelineForVideo(subclip_seconds=0.5)


if __name__ == "__main__":
    pipeline()
