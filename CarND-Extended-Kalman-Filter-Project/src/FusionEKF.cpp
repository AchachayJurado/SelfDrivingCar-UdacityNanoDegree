#include "FusionEKF.h"
#include "Eigen/Dense"
#include "tools.h"
#include <iostream>

using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::cout;
using std::endl;
using std::vector;

/**
 * Constructor.
 */
FusionEKF::FusionEKF()
{
  is_initialized_ = false;

  previous_timestamp_ = 0;

  // initializing matrices
  R_laser_ = MatrixXd(2, 2);
  R_radar_ = MatrixXd(3, 3);
  H_laser_ = MatrixXd(2, 4);
  Hj_ = MatrixXd(3, 4);

  //measurement covariance matrix - laser
  R_laser_ << 0.0225, 0,
      0, 0.0225;

  //measurement covariance matrix - radar
  R_radar_ << 0.09, 0, 0,
      0, 0.0009, 0,
      0, 0, 0.09;

  //measurement covariance matrix
  H_laser_ << 1, 0, 0, 0,
      0, 1, 0, 0;

  noise_ax_ = 9.0;
  noise_ay_ = 9.0;

  //  Create a 4D state vector, the values of the x state are not known yet
  VectorXd x = VectorXd(4);
  x << 0.0, 0.0, 1.0, 1.0;

  // The initial matrix F_
  MatrixXd F = MatrixXd(4, 4);
  F << 1, 0, 0.5, 0,
      0, 1, 0, 0.5,
      0, 0, 1, 0,
      0, 0, 0, 1;

  MatrixXd Q = MatrixXd::Zero(4, 4);
  MatrixXd P = MatrixXd::Zero(4, 4);

  ekf_.Init(x, P, F, H_laser_, R_laser_, Q);
}

/**
 * Destructor.
 */
FusionEKF::~FusionEKF() {}

void FusionEKF::ProcessMeasurement(const MeasurementPackage &measurement_pack)
{
  /**
   * Initialization
   */
  if (!is_initialized_)
  {
    // First measurement
    cout << "EKF: " << endl;

    ekf_.x_ = VectorXd(4);
    ekf_.x_ << 1, 1, 1, 1;

    if (measurement_pack.sensor_type_ == MeasurementPackage::RADAR)
    {
      // Convert from polar to cartesian coordinates
      float ro = measurement_pack.raw_measurements_[0];
      float theta = measurement_pack.raw_measurements_[1];
      float ro_dot = measurement_pack.raw_measurements_[2];

      float px = cos(theta) * ro;
      float py = sin(theta) * ro;
      float vx = cos(theta) * ro_dot;
      float vy = sin(theta) * ro_dot;

      // The speed is certain
      ekf_.P_ << 1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1, 0,
          0, 0, 0, 1;

      ekf_.x_ << px, py, vx, vy;
    }
    else if (measurement_pack.sensor_type_ == MeasurementPackage::LASER)
    {
      float px = measurement_pack.raw_measurements_[0];
      float py = measurement_pack.raw_measurements_[1];

      // The speed is certain
      ekf_.P_ << 1, 0, 0, 0,
          0, 1, 0, 0,
          0, 0, 1000, 0,
          0, 0, 0, 1000;

      ekf_.x_ << px, py, 0, 0;
    }

    // done initializing, no need to predict or update
    is_initialized_ = true;
    return;
  }

  // compute the time elapsed between the current and previous measurements
  float dt = (measurement_pack.timestamp_ - previous_timestamp_) / 1000000.0; // dt - expressed in seconds
  previous_timestamp_ = measurement_pack.timestamp_;

  /**
   * Prediction
   */

  // Modify the F matrix so that the time is integrated
  ekf_.F_(0, 2) = dt;
  ekf_.F_(1, 3) = dt;

  // set the process covariance matrix Q
  ekf_.Q_ = tools.CalculateCovariantMatrix(dt, noise_ax_, noise_ay_);

  ekf_.Predict();

  /**
   * Update
   */

  if (measurement_pack.sensor_type_ == MeasurementPackage::RADAR)
  {
    ekf_.H_ = tools.CalculateJacobian(ekf_.x_);
    ekf_.R_ = R_radar_;
    ekf_.UpdateEKF(measurement_pack.raw_measurements_);
  }
  else
  {
    ekf_.H_ = H_laser_;
    ekf_.R_ = R_laser_;
    ekf_.Update(measurement_pack.raw_measurements_);
  }

  // print the output
  cout << "x_ = " << ekf_.x_ << endl;
  cout << "P_ = " << ekf_.P_ << endl;
}
