# Extended Kalman Filter Project


In this project a kalman filter has been developed to estimate the state of a moving object of interest with noisy lidar and radar measurements.

One of the requirements is that the obtained RMSE values are lower than the tolerance [.11, .11, 0.52, 0.52].

After the //TODO: has been removed and all the missing implementation in the EKF is finished, it must be tested using the [Term 2 Simulator](https://github.com/udacity/self-driving-car-sim/releases).

In order to create the communication between the simulator and the EKF output, a binary is to be created and run, following the steps:
1. mkdir build
2. cd build
3. cmake ..
4. make
5. ./ExtendedKF

The communication protocol that main.cpp uses for uWebSocketIO in communicating with the simulator is as follows:


**INPUT**: values provided by the simulator to the c++ program

["sensor_measurement"] => the measurement that the simulator observed (either lidar or radar)


**OUTPUT**: values provided by the c++ program to the simulator

["estimate_x"] <= kalman filter estimated position x

["estimate_y"] <= kalman filter estimated position y

["rmse_x"]

["rmse_y"]

["rmse_vx"]

["rmse_vy"]

__COMMAND LINE OUTPUT:__
I have added some couts in order to see the estimated x and the RMSE corresponding to it, also ti visualy obbserve the update after a new measurement from Lidar or Radar has come in.
```
x_ =  11.1315
      14.1753
     -4.86447
      0.406382
P_ =  0.00687678  -0.0025531   0.0173722 -0.00788902
     -0.0025531  0.00562724 -0.00880071   0.0129621
      0.0173722 -0.00880071    0.115152  -0.0401013
     -0.00788902   0.0129621  -0.0401013    0.095715
RMSE = 0.0740899
       0.0964326
       0.446976
       0.476035
UpdateEKF (Radar)  18.0394
                   0.897837
                  -3.23191
x_ =  10.8881
      14.1617
     -4.98471
       0.14773
P_ =  0.00845673 -0.00358964   0.0216488  -0.0113006
      -0.00358964  0.00639669   -0.012797   0.0137597
        0.0216488   -0.012797    0.123281  -0.0578884
       -0.0113006   0.0137597  -0.0578884   0.0862289
RMSE = 0.0740244
       0.0963655
       0.446603
       0.475599
Update (Laser)  10.468
                14.0591
```

### Results
_Data Set 1_
<img src="./report_images/ekf_dataset1.png" width="800"/>

_Data Set 2_
<img src="./report_images/ekf_dataset2.png" width="800"/>

For both cases the values of RMSE are lower than the specified tolerance.
RMSE(x)  < 0.11
RMSE(y)  < 0.11
RMSE(Vx) < 0.52
RMSE(Vy) < 0.52

See [project rubrics](https://review.udacity.com/#!/rubrics/1962/view)


### References
The material from the Self Driving Car Nanodegree (Sensor Fusion and Extended Kalman Filter) have been used for development of this code.
Find the relevant fomulas [here](https://video.udacity-data.com/topher/2018/June/5b327c11_sensor-fusion-ekf-reference/sensor-fusion-ekf-reference.pdf).

---

## Other Important Dependencies

* cmake >= 3.5
  * All OSes: [click here for installation instructions](https://cmake.org/install/)
* make >= 4.1 (Linux, Mac), 3.81 (Windows)
  * Linux: make is installed by default on most Linux distros
  * Mac: [install Xcode command line tools to get make](https://developer.apple.com/xcode/features/)
  * Windows: [Click here for installation instructions](http://gnuwin32.sourceforge.net/packages/make.htm)
* gcc/g++ >= 5.4
  * Linux: gcc / g++ is installed by default on most Linux distros
  * Mac: same deal as make - [install Xcode command line tools](https://developer.apple.com/xcode/features/)
  * Windows: recommend using [MinGW](http://www.mingw.org/)

## Code Style

I have tried to stick to [Google's C++ style guide](https://google.github.io/styleguide/cppguide.html).

### Future work
The EKF has several applications and I would like to improve my code in the shape of a library that can be extended for other use cases or for more sensor inputs.
