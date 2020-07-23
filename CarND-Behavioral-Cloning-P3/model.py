import csv
import theano.ifelse

from natwork import NvidiaNet
from utils import *

import keras
print('keras: %s' % keras.__version__) # it is important that the keras version is the same when training the network
                                       # than when testing the model in autonomous mode

"""
----------------------------------------------------------------------------------------------------
To create the model.5 run this script and choose the input DATASET, the hyper parameters:
EPOCHS and BATCH_SIZE and the training data augmentation parameters: AUGMENT BY FLIPPING,
SIDE CAMERAS ON, VALIDATION SAMPLES.
----------------------------------------------------------------------------------------------------
"""

# DATASET_CSV = './record_simulator/track1/driving_log.csv'
DATASET_CSV = './record_simulator/track2/driving_log.csv'

# Network hyper parameter configuration
EPOCHS = 3
BATCH_SIZE = 32

# Parameters for training data augmentation
AUGMENT_BY_FLIPPING = True
SIDE_CAMERAS_ON = True
VALIDATION_SAMPLES = 0.2 # 20% of the DATASET is used for validation and 80% for training


def run_model():

    # Get the data used to train the network
    # [TRAINING DATA SET 1] 8 loop driving in both directions in track 1
    # [TRAINING DATA SET 2] 2 laps driving in one direction in track 2
    # All data is merged into a common csv file containing the relevant tokens

    samples = []
    with open(DATASET_CSV) as csvfile:
        reader = csv.reader(csvfile)
        for line in reader:
            samples.append(line)

    # Separate the training data from the validation data
    training_samples, validation_samples = train_test_split(samples, test_size=VALIDATION_SAMPLES, shuffle=True)

    # Training Data Stadistics Visualization
    print("Sample Size "+str(len(samples)))
    print("Training Sample Size "+str(len(training_samples)))
    print("Validation Sample Size "+str(len(validation_samples)))

    print("Augment by Flipping: " + str(AUGMENT_BY_FLIPPING))
    print("Side Cameras On: " + str(SIDE_CAMERAS_ON))

    sampleFactor = getSampleFactor()
    print("Sample Factor: " + str(sampleFactor))
    print("Number of augmented training images "+str(len(training_samples) * sampleFactor))
    print("Number of augmented validation images "+str(len(validation_samples) * sampleFactor))

    # Generators for the training and validation data
    training_generator = data_generator(training_samples, batch_size=BATCH_SIZE)
    validation_generator = data_generator(validation_samples, batch_size=BATCH_SIZE)

    # Model creation
    model = NvidiaNet()

    # Model Training
    sampleFactor = getSampleFactor()
    model.compile(loss='mse', optimizer='adam')
    model.fit_generator(training_generator, samples_per_epoch=len(training_samples)*sampleFactor, validation_data=validation_generator, nb_val_samples=len(validation_samples)*sampleFactor, nb_epoch=EPOCHS, verbose=1)

    # Save Model
    model.save('model.h5')

    return

if __name__ == '__main__':
    run_model()
