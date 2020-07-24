#include "kalman_filter.h"
#include <iostream>
using Eigen::MatrixXd;
using Eigen::VectorXd;

/*
 * Please note that the Eigen library does not initialize
 *   VectorXd or MatrixXd objects with zeros upon creation.
 */

KalmanFilter::KalmanFilter() {}

KalmanFilter::~KalmanFilter() {}

Eigen::MatrixXd I_; // Identity matrix

void KalmanFilter::Init(VectorXd &x_in, MatrixXd &P_in, MatrixXd &F_in,
                        MatrixXd &H_in, MatrixXd &R_in, MatrixXd &Q_in)
{
  x_ = x_in;
  P_ = P_in;
  F_ = F_in;
  H_ = H_in;
  R_ = R_in;
  Q_ = Q_in;
  I_ = MatrixXd::Identity(P_.rows(), P_.cols());
}

void KalmanFilter::Predict()
{
  x_ = F_ * x_; // we assume that u (the mean of noise) is zero
  MatrixXd Ft = F_.transpose();
  P_ = F_ * P_ * Ft + Q_;
}

void KalmanFilter::Update(const VectorXd &z)
{
  std::cout << "Update (Laser) " << z << std::endl;
  VectorXd z_pred = H_ * x_;
  VectorXd y = z - z_pred;

  UpdateCommon(y);
}

void KalmanFilter::UpdateEKF(const VectorXd &z)
{
  std::cout << "UpdateEKF (Radar) " << z << std::endl;
  float px = x_(0);
  float py = x_(1);
  float vx = x_(2);
  float vy = x_(3);

  double rho = sqrt(px * px + py * py);
  if (rho < .00001)
  {
    px += .001;
    py += .001;
    rho = sqrt(px * px + py * py);
  }
  double theta = atan2(py, px);
  double rho_dot = (px * vx + py * vy) / rho;
  VectorXd h = VectorXd(3);
  h << rho, theta, rho_dot;

  VectorXd y = z - h;

  // make sure that the angle is between -pi and pi
  for (; y(1) < -M_PI; y(1) += 2 * M_PI)
  {
  }
  for (; y(1) > M_PI; y(1) -= 2 * M_PI)
  {
  }

  UpdateCommon(y);
}

void KalmanFilter::UpdateCommon(const VectorXd &y)
{
  MatrixXd Ht = H_.transpose();
  MatrixXd S = H_ * P_ * Ht + R_;
  MatrixXd Si = S.inverse();
  MatrixXd PHt = P_ * Ht;
  MatrixXd K = PHt * Si;

  // new estimate
  x_ = x_ + (K * y);
  P_ = (I_ - K * H_) * P_;
}
