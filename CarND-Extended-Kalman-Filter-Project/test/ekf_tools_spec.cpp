#include "../src/tools.h"
#include "gtest/gtest.h"

using Eigen::MatrixXd;
using Eigen::VectorXd;
using std::vector;

constexpr float DELTA_E = 0.001;

TEST(tools_test, CalculateRMSE_GivenEstimationAndGroundTruth_ExpectValidRMSE)
{
 vector<VectorXd> estimations;
 vector<VectorXd> ground_truth;

 // Append estimations and ground truth values
 VectorXd e(4);
 VectorXd g(4);
 e << 1.0, 1.0, 0.2, 0.1;
 g << 1.1, 1.1, 0.3, 0.2;
 estimations.push_back(e);
 ground_truth.push_back(g);

 e << 2.0, 2.0, 0.3, 0.2;
 g << 2.1, 2.1, 0.4, 0.3;
 estimations.push_back(e);
 ground_truth.push_back(g);

 e << 3.0, 3.0, 0.4, 0.3;
 g << 3.1, 3.1, 0.5, 0.4;
 estimations.push_back(e);
 ground_truth.push_back(g);

 Tools tools{};
 const auto rmse = tools.CalculateRMSE(estimations, ground_truth);
 VectorXd expected(4);
 expected << 0.1, 0.1, 0.1, 0.1;
 EXPECT_TRUE(rmse.isApprox(expected, DELTA_E));
}

TEST(tools_test, CalculateJacobian_GivenStateVector_ExpectValidJacobian)
{
 VectorXd x_predicted(4);
 x_predicted << 1.0, 2.0, 0.2, 0.4;

 Tools tools{};
 MatrixXd Hj = tools.CalculateJacobian(x_predicted);
 MatrixXd expected(3, 4);
 expected << 0.447214, 0.894427, 0.0, 0.0, //
     -0.4, 0.2, 0.0, 0.0,                  //
     0.0, 0.0, 0.447214, 0.894427;

 EXPECT_TRUE(Hj.isApprox(expected, DELTA_E));
}
