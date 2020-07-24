#ifndef TOOLS_H_
#define TOOLS_H_

#include "Eigen/Dense"
#include <vector>

class Tools
{
public:
  /**
   * Constructor.
   */
  Tools();

  /**
   * Destructor.
   */
  virtual ~Tools();

  /**
   * A helper method to calculate RMSE.
   */
  Eigen::VectorXd CalculateRMSE(const std::vector<Eigen::VectorXd> &estimations,
                                const std::vector<Eigen::VectorXd> &ground_truth);

  /**
   * A helper method to calculate Jacobians.
   */
  Eigen::MatrixXd CalculateJacobian(const Eigen::VectorXd &x_state);

  /**
   * A helper method to calculate the covariant matrix Q.
   */
  Eigen::MatrixXd CalculateCovariantMatrix(const double dt, const double noise_ax, const double noise_ay);
};

#endif // TOOLS_H_
