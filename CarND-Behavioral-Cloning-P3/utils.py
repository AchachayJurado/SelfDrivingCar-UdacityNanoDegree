import cv2
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split

# Parameters for training data augmentation
AUGMENT_BY_FLIPPING = True
SIDE_CAMERAS_ON = True
CORRECTION = 0.2
BATCH_SIZE = 32

# IMG_DIR = 'record_simulator/track1/IMG/'
IMG_DIR = 'record_simulator/track2/IMG/'

"""
=== Python generator used to provide data ===
* To avoid out of memory exception in case of big training sets.
"""
def data_generator(samples, batch_size=BATCH_SIZE):
    num_samples = len(samples)
    while 1: # Loop forever so the generator never terminates
        sklearn.utils.shuffle(samples)
        for offset in range(0, num_samples, batch_size):
            batch_samples = samples[offset:offset+batch_size]

            images = []
            angles = []
            for batch_sample in batch_samples:
                addSample(images, angles, batch_sample)

            # Trim image to focus on interesting part of the road
            X_train = np.array(images)
            y_train = np.array(angles)
            yield sklearn.utils.shuffle(X_train, y_train)
    return


"""
=== Calculates the final size of the training samples ===
Based on additions due to flipping images and side cameras on.
"""
def getSampleFactor():
    sampleFactor = 1
    if (AUGMENT_BY_FLIPPING):
        sampleFactor = 2

    if (SIDE_CAMERAS_ON):
        sampleFactor = sampleFactor * 3

    return sampleFactor

"""
=== Add training or validation data based ===
From the driving_log.csv description of a sample, the format is:
sample[0]: center_image
sample[1]: left_image
sample[2]: right_image
sample[3]: steering_angle
If AUGMENT_BY_FLIPPING==True, then a flipped image and angle is added
If SIDE_CAMERAS_ON==True then the data from the left and right camera is added.
"""
def addSample(images, angles, sample):
    # Add sample data from the camera located at the center
    center_image = getimage(sample[0])
    center_angle = float(sample[3])
    addImage(images, angles, center_image, center_angle)

    # Adding sample data from left and right side cameras
    if (SIDE_CAMERAS_ON):
        left_image = getimage(sample[1])
        addImage(images, angles, left_image, center_angle+CORRECTION)

        right_image = getimage(sample[2])
        addImage(images, angles, right_image, center_angle-CORRECTION)
    return

"""
=== Improving the training/validation set ===
* Adds an image and an angle to the training or validation set.
* Adds a flipped image to avoid bias.
"""
def addImage(images, angles, image, angle):
    images.append(image)
    angles.append(angle)
    if(AUGMENT_BY_FLIPPING):
        images.append(cv2.flip(image,1))
        angles.append(-angle)
    return

"""
=== Read image identified by the last segment path ===
Note: The image is expected in folder specified in parameter IMG_DIR
"""
def getimage(source_path):
    filename = source_path.split('/')[-1]
    current_path = IMG_DIR + filename
    image = cv2.imread(current_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image
