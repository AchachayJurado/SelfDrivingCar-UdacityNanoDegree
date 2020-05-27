import math

# Image Processing
import matplotlib.image as mpimg

# Video Processing
from moviepy.editor import VideoFileClip
from IPython.display import HTML

from utils import *


def FindEgoLanes(images_directory, return_process):

    total_images = len(os.listdir(images_directory))
    image_number = 1

    for filename in os.listdir(images_directory):

        original_image = mpimg.imread(images_directory + filename)

        # GetImageSize(image)
        image = mpimg.imread('test_images/solidWhiteRight.jpg')
        xsize = image.shape[1]
        ysize = image.shape[0]
        color_select = np.copy(image)
        line_image = np.copy(image)
        print("---------------------------------------------------")
        print("Image ", image_number, filename,
              "has dimensions:", xsize, ysize)

        # Process images:
        [gray_image, blur_image, canny_image, region_of_interest,
            lines_in_image, ego_lanes_image] = ProcessImage(original_image, xsize, ysize, return_process)

        # Plot original images vs. processed images:
        PlotOriginalAndProcessed(
            filename, total_images, original_image, ego_lanes_image, image_number)

        # Plot Images with Ego Lane:
        PlotLaneFindingProcess(filename, gray_image, blur_image, canny_image,
                               region_of_interest, lines_in_image, ego_lanes_image, image_number)
        image_number += 1

        # Show process of ego lane finding for each image
        # plt.show()
    if return_process:
        print("---------------------------------------------------")
        print(total_images,
              "images were processed, find the results in test_images_output/")


def FindEgoLanesVideo(videos_directory):
    total_videos = len(os.listdir(videos_directory))
    video_number = 1

    for filename in os.listdir(videos_directory):
        image = mpimg.imread('test_images/solidWhiteRight.jpg')

        def process_image(image):
            processed_image = ProcessImage(
                image, image.shape[1], image.shape[0], False)
            return processed_image

        print("---------------------------------------------------")
        print("Video ", video_number, filename)

        clips = VideoFileClip("test_videos/"+filename)
        video_output = 'test_videos_output/process_'+filename
        line_clips = clips.fl_image(process_image)
        line_clips.write_videofile(video_output, audio=False)
        HTML(
            """<video width="480" height="270" controls><source src="{0}"></video>""".format(video_output))
        video_number += 1

    print("---------------------------------------------------")
    print(total_videos, "videos were processed, find the results in test_videos_output/")


# Define directories and Tasks to be excecuted
images_directory = "test_images/"
FindEgoLanes(images_directory, return_process=True)

videos_directory = "test_videos/"
FindEgoLanesVideo(videos_directory)
