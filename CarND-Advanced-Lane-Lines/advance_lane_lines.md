## Advanced Lane Lines

The goals / steps of this project are the following:

* Compute the camera calibration matrix and distortion coefficients given a set of chessboard images.
* Apply a distortion correction to raw images.
* Use color transforms, gradients, etc., to create a thresholded binary image.
* Apply a perspective transform to rectify binary image ("birds-eye view").
* Detect lane pixels and fit to find the lane boundary.
* Determine the curvature of the lane and vehicle position with respect to center.
* Warp the detected lane boundaries back onto the original image.
* Output visual display of the lane boundaries and numerical estimation of lane curvature and vehicle position.

[//]: # (Image References)

[image0]: ./output_images/calibrated_calibration3.jpg "Single Image Calibration"
[image1]: ./output_images/distortion_correction_test2.jpg "Undistorted"
[image2]: ./examples/undistort_output.png "Undistorted"
[image3]: ./test_images/test1.jpg "Road Transformed"
[image4]: ./examples/binary_combo_example.jpg "Binary Example"
[image5]: ./examples/warped_straight_lines.jpg "Warp Example"
[image6]: ./examples/color_fit_lines.jpg "Fit Visual"
[image7]: ./examples/example_output.jpg "Output"
[video1]: ./project_video.mp4 "Video"

---

### Camera Calibration

The camera calibration function is contained in the `camera_calibration.py` in the method `Camera`.

#### Calibration Process
1. Preparing the "object points", which will be the (x,y,z) coordinates of the chessboard corners.
  I am assuming that the chessboard is fixed to on plane (x, y), therefore z=0. This is done so that the object points are the same for each calibration image.
2. Iterating through the calibration images to look for corners using `cv2.findChessboardCorners()` on gray images.
3. In case corners are detected an objpoint will be appended to a list of matches: `objpoints` for 3D and `imgpoints` for 2D points.
  The `objpoint` is a replicated aarray of coordinates.
4. In order to keep all the 2D and 3D points found, a pickel file is created.
5. At the end those output `objpoints` and `imgpoints` are used to computer the camera calibration and distortion coefficients using `Camera.getCalibration()`
  method with the usage of `cv2.   calibrateCamera` function. This computation depends only on the image size, which is cached from the last image (width, height).

The distortion correction is applied to the test images using the `Camera.undistrot` method running `cv2.undistort()` function to obtain the results:
  <p align="center">
  <img width="460" height="300" src="./output_images/chessboard_calibration.png">
</p>

Here an example of a single image calibration
![single image camera calibration][image0]


An example of the distortion correction can be found on the next section.
### Pipeline (single images)

#### 1. Provide an example of a distortion-corrected image.
The `cv2.undistort()` function is used in order to create the distortion correction.
I chose this road image example, because the distortion correction is more visible due to the traffic sign on the left side. Notice the left image, it seems that the camera is leaning to the left side, and on the right image, it is centered.
![single image camera calibration][image1]
The distortion correction is more obvious in the chessboard images, for instance:
  <p align="center">
  <img width="600" height="200" src="./output_images/distortion_correction_calibration1.jpg">
</p>

#### 2. Describe how (and identify where in your code) you used color transforms, gradients or other methods to create a thresholded binary image.  Provide an example of a binary image result.

I used a combination of color and gradient thresholds to generate a binary image (thresholding steps at lines # through # in `another_file.py`).  Here's an example of my output for this step.  (note: this is not actually from one of the test images)

![alt text][image3]

#### 3. Describe how (and identify where in your code) you performed a perspective transform and provide an example of a transformed image.

The code for my perspective transform includes a function called `warper()`, which appears in lines 1 through 8 in the file `example.py` (output_images/examples/example.py) (or, for example, in the 3rd code cell of the IPython notebook).  The `warper()` function takes as inputs an image (`img`), as well as source (`src`) and destination (`dst`) points.  I chose the hardcode the source and destination points in the following manner:

```python
src = np.float32(
    [[(img_size[0] / 2) - 55, img_size[1] / 2 + 100],
    [((img_size[0] / 6) - 10), img_size[1]],
    [(img_size[0] * 5 / 6) + 60, img_size[1]],
    [(img_size[0] / 2 + 55), img_size[1] / 2 + 100]])
dst = np.float32(
    [[(img_size[0] / 4), 0],
    [(img_size[0] / 4), img_size[1]],
    [(img_size[0] * 3 / 4), img_size[1]],
    [(img_size[0] * 3 / 4), 0]])
```

This resulted in the following source and destination points:

| Source        | Destination   |
|:-------------:|:-------------:|
| 585, 460      | 320, 0        |
| 203, 720      | 320, 720      |
| 1127, 720     | 960, 720      |
| 695, 460      | 960, 0        |

I verified that my perspective transform was working as expected by drawing the `src` and `dst` points onto a test image and its warped counterpart to verify that the lines appear parallel in the warped image.

![alt text][image4]

#### 4. Describe how (and identify where in your code) you identified lane-line pixels and fit their positions with a polynomial?

Then I did some other stuff and fit my lane lines with a 2nd order polynomial kinda like this:

![alt text][image5]

#### 5. Describe how (and identify where in your code) you calculated the radius of curvature of the lane and the position of the vehicle with respect to center.

I did this in lines # through # in my code in `my_other_file.py`

#### 6. Provide an example image of your result plotted back down onto the road such that the lane area is identified clearly.

I implemented this step in lines # through # in my code in `yet_another_file.py` in the function `map_lane()`.  Here is an example of my result on a test image:

![alt text][image6]

---

### Pipeline (video)

#### 1. Provide a link to your final video output.  Your pipeline should perform reasonably well on the entire project video (wobbly lines are ok but no catastrophic failures that would cause the car to drive off the road!).

Here's a [link to my video result](./project_video.mp4)

---

### Discussion

#### 1. Briefly discuss any problems / issues you faced in your implementation of this project.  Where will your pipeline likely fail?  What could you do to make it more robust?

Here I'll talk about the approach I took, what techniques I used, what worked and why, where the pipeline might fail and how I might improve it if I were going to pursue this project further.
