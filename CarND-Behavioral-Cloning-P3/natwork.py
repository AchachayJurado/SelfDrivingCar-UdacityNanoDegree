from keras.models import Sequential
from keras.layers import Flatten, Dense, Dropout, Lambda, Cropping2D
from keras.layers.convolutional import Conv2D
import theano.ifelse

"""
-----------------------------------------
----  Implementation of a NvidiaNet  ----
-----------------------------------------
Based on the CNN architecture described in
https://developer.nvidia.com/blog/deep-learning-self-driving-cars/
In addition to the original network, dropouts were added in the fully connected layers to reduce overfitting.
The original size and the cropping size are parametrizable.
"""

# Parameters:
## Original Image Size
ORIGINAL_X = 160
ORIGINAL_Y = 320
ORIGINAL_CHANNELS = 3

## Cropping Image
CROP_X_TOP = 60
CROP_X_BOTTOM = 25

def NvidiaNet() :

    model = Sequential()

    # **================**
    # ** --- Layer 0 ---**
    # **================**
    # Image Cropping (Data Preparation)
    # To select only the area of interest, the imaged is cropped at top and bottom

    # input shape (160,320,3) --> output shape = (75, 320, 3)
    model.add(Cropping2D(cropping=((CROP_X_TOP, CROP_X_BOTTOM), (0,0)), input_shape=(ORIGINAL_X, ORIGINAL_Y, ORIGINAL_CHANNELS)))

    # **================**
    # ** --- Layer 1 ---**
    # **================**
    # Image Normalization
    # The normalizer is hardcoded and does not have adjustment to the learning process.

    # input shape (75, 320, 3) -> output shape NORMALIZED(75, 320, 3)
    model.add(Lambda(lambda x: (x / 127.5) - 1))

    # **================**
    # **  Layers 2 - 6  **
    # **================**
    # Convolutional layers (5 layers)
    # Designed to perform feature extraction, chosen empirically through a series of experiments.

    # Strided Convolutions with a 2x2 stride and a 5x5 kernel
    model.add(Conv2D(24, (5, 5), activation= "relu", strides=(2, 2)))
    model.add(Conv2D(36, (5, 5), activation= "relu", strides=(2, 2)))
    model.add(Conv2D(48, (5, 5), activation= "relu", strides=(2, 2)))

    # Non strided convolutions with a 3x3 kernel size
    model.add(Conv2D(64, (3, 3), activation= "relu"))
    model.add(Conv2D(64, (3, 3), activation= "relu"))

    # **================**
    # ** --- Layer 7 ---**
    # **================**
    # Flatten layer
    model.add(Flatten())

    # **================**
    # **  Layers 8 -10  **
    # **================**
    # Fully Connected layers with dropout leading to a final output control value which is inverse-turning-radius.

    # 100 neurons
    model.add(Dense(100))
    model.add(Dropout(0.3))

    # 50 neurons
    model.add(Dense(50))
    model.add(Dropout(0.3))

    # 10 neurons
    model.add(Dense(10))
    model.add(Dropout(0.3))

    # Final Output-Control Value for **STEERING**

    model.add(Dense(1))
    return model
