import os
import glob
import cv2
import time
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
from moviepy.editor import VideoFileClip
from IPython.display import HTML


from perception.undistorter import *
from perception.camera_calibration import *
from perception.tresholder import *
from perception.pespective_transformer import *
from perception.lane_finder import *
from perception.save import *

TEST_IMAGES = glob.glob("test_images/*.jpg")
TEST_VIDEOS = glob.glob("test_videos/*.mp4")


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


class Profiler(object):
    def __init__(self, name):
        self.name = name
        self.elapsed = 0
        self.start_time = None

    def start(self):
        self.start_time = time.time()

    def update(self):
        self.elapsed += time.time() - self.start_time

    def fmt_timedelta(self, delta):
        return str(delta).split(".")[0]

    def fmt_seconds(self, seconds):
        return self.fmt_timedelta(timedelta(seconds=seconds))

    def get_elapsed(self):
        return self.elapsed

    def get_elapsed_str(self):
        return self.fmt_seconds(self.elapsed)

    def display_elapsed(self, total):
        percent = 100 * self.elapsed / total
        name = self.name.ljust(30)
        elapsed = self.get_elapsed_str()

    def display_processing_factor(self, original_secs):
        factor = self.elapsed / original_secs


class LaneLinesTracker(object):
    def __init__(self):
        self.camera = GetCalibratedCamera()
        self.warper = Warper()

        # profiling
        self.p_video = Profiler("Total Time")
        self.p_undistort = Profiler("Distortion  Correction")
        self.p_edges = Profiler("Edge Detection")
        self.p_warp = Profiler("Perspective Transform")
        self.p_fitting = Profiler("Lane Fitting")
        self.p_overlay = Profiler("Overlay Drawing")

    def process_video(self, input_file, output_file, subclip_seconds=None):
        # delete output file to avoid permission problems between docker/user on write
        delete_file(output_file)

        self.p_video.start()

        # read
        clip = VideoFileClip(input_file)

        # subclip
        if subclip_seconds:
            clip = clip.subclip(0, subclip_seconds)

        # set image handler
        clip = clip.fl_image(self.process_image)

        # process / save
        clip.write_videofile(output_file, audio=False, verbose=False)
        chmod_rw_all(output_file)
        self.p_video.update()

        # display profiling results
        total_secs = self.p_video.get_elapsed()
        self.p_video.display_elapsed(total_secs)
        self.p_undistort.display_elapsed(total_secs)
        self.p_edges.display_elapsed(total_secs)
        self.p_warp.display_elapsed(total_secs)
        self.p_fitting.display_elapsed(total_secs)
        self.p_overlay.display_elapsed(total_secs)
        self.p_video.display_processing_factor(clip.duration)

    def draw_overlay(self, lane_fitting, undistorted, warped):
        # get curvature and vehicle position
        left_cr, right_cr = lane_fitting.get_curvature()
        offset_kpi = abs(lane_fitting.get_vehicle_position())

        # get fitpoints
        pts_y, left_fitx, right_fitx = lane_fitting.get_fitpoints()

        # Create an image to draw the lines on
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
        overlay = self.warper.unwarp(color_warp)

        # Combine the result with the original image
        vis_overlay = cv2.addWeighted(undistorted, 1, overlay, 0.3, 0)

        curvature = 0.5*(left_cr/1000 + right_cr/1000)

        cr_text = "Radius of Curvature:  " + '{:6.2f}km'.format(
            curvature)
        pos_text = "Distance from Center: " + '{:6.2f}cm'.format(
            offset_kpi*100)

        def put_text(image, text, color=(0, 0, 255), ypos=100):
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(image, text, (430, ypos),
                        font, 1, color, 2, cv2.LINE_AA)

        put_text(vis_overlay, cr_text, ypos=660)
        put_text(vis_overlay, pos_text, ypos=700)

        return vis_overlay

    def process_image(self, image):
        # Distortion correction
        self.p_undistort.start()
        undistorted = self.camera.undistort(image)
        self.p_undistort.update()

        # Edge Detection
        self.p_edges.start()
        edge_detector = EdgeDetector()
        edges = edge_detector.detect(undistorted)
        self.p_edges.update()

        # Perspective Transform
        self.p_warp.start()
        warped = self.warper.warp(edges)
        self.p_warp.update()

        # Lane Fitting
        self.p_fitting.start()
        lane_fitting = LaneFitter(image.shape[1], image.shape[0])
        vis_lanes = lane_fitting.fit_polynomial(warped)
        self.p_fitting.update()

        # Draw Overlay
        self.p_overlay.start()
        vis_overlay = self.draw_overlay(lane_fitting, undistorted, warped)
        self.p_overlay.update()

        return vis_overlay


def RunPipelineForVideo(subclip_seconds=None):

    print(TEST_VIDEOS)
    for idx, filename in enumerate(sorted(TEST_VIDEOS)):

        tracker = LaneLinesTracker()

        print("---------------------------------------------------")
        print("Video ", filename)

        clips = VideoFileClip(filename)
        video_output = 'output_' + filename
        clip = tracker.process_video(filename, video_output, subclip_seconds)
        HTML(
            """<video width="480" height="270" controls><source src="{0}"></video>""".format(video_output))
