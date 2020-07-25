#include "tools.h"
#include <iostream>

using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::vector;

Tools::Tools() {}

Tools::~Tools() {}

VectorXd Tools::CalculateRMSE(const vector<VectorXd> &estimations,
                              const vector<VectorXd> &ground_truth)
{
   VectorXd rmse(4);
   rmse << 0.0, 0.0, 0.0, 0.0;

   // check the validity of the following inputs:
   //  * Estimation vector size should not be zero
   //  * Estimation vector size should equal ground truth vector size
   if (estimations.size() != ground_truth.size() || estimations.size() == 0)
   {
      std::cout << "Invalid estimation or ground_truth data" << std::endl;
      return rmse;
   }

   // Accumulate squared residuals
   for (unsigned int i = 0; i < estimations.size(); ++i)
   {
      VectorXd residual = estimations[i] - ground_truth[i];

      // Coefficient-wise multiplication
      residual = residual.array() * residual.array();
      rmse += residual;
   }

   // calculate the mean
   rmse = rmse / estimations.size();

   // calculate the squared root
   rmse = rmse.array().sqrt();

   std::cout << "RMSE = " << rmse << std::endl;
   // return the result
   return rmse;
}

MatrixXd Tools::CalculateJacobian(const VectorXd &x_state)
{
   MatrixXd Hj(3, 4);
   // recover state parameters
   float px = x_state(0);
   float py = x_state(1);
   float vx = x_state(2);
   float vy = x_state(3);

   // pre-compute a set of terms to avoid repeated calculation
   float c1 = px * px + py * py;

   // avoid division by zero
   if (fabs(c1) < 0.0001)
   {
      px += 0.0001;
      py += 0.0001;
      c1 = px * px + py * py;
   }
   float c2 = sqrt(c1);
   float c3 = (c1 * c2);

   // compute the Jacobian matrix
   Hj << (px / c2), (py / c2), 0, 0,
       -(py / c1), (px / c1), 0, 0,
       py * (vx * py - vy * px) / c3, px * (px * vy - py * vx) / c3, px / c2, py / c2;

   return Hj;
}

MatrixXd Tools::CalculateCovariantMatrix(const double dt, const double noise_ax, const double noise_ay)
{
   MatrixXd Q(4, 4);

   const double dt2 = dt * dt;
   const double dt3 = dt * dt2;
   const double dt4 = dt * dt3;

   const double r11 = dt4 * noise_ax / 4;
   const double r13 = dt3 * noise_ax / 2;
   const double r22 = dt4 * noise_ay / 4;
   const double r24 = dt3 * noise_ay / 2;
   const double r31 = dt3 * noise_ax / 2;
   const double r33 = dt2 * noise_ax;
   const double r42 = dt3 * noise_ay / 2;
   const double r44 = dt2 * noise_ay;

   Q << r11, 0.0, r13, 0.0,
       0.0, r22, 0.0, r24,
       r31, 0.0, r33, 0.0,
       0.0, r42, 0.0, r44;

   return Q;
}
