#ifndef CAR_CONTROLLER_H
#define CAR_CONTROLLER_H

#include "PID.h"

class CarController
{
public:
 CarController()
 {
  // Initialize controllers for steering and acceleration
  steering_controller_.Init(0.1, 0.00, 0.02);
  throttle_controller_.Init(0.6, 0.01, 0.01);

  // Set limits for both controllers
  steering_controller_.SetLimits(-1.0, 1.0);
  throttle_controller_.SetLimits(-1.0, 1.0);

  // Set target speed
  target_speed_mph_ = min_speed_mph_;
 }

 void Update()
 {
  UpdateTargetSpeed();

  double speed_error = target_speed_mph_ - current_speed_mph_;
  throttle_controller_.UpdateError(speed_error);
  steering_controller_.UpdateError(-1.0 * current_cte_);
 }

 void UpdateTargetSpeed()
 {
  if (min_throttle_ < current_cte_ and current_cte_ < max_throttle_)
  {
   target_speed_mph_ += speed_delta_mph_;
  }
  else
  {
   target_speed_mph_ -= speed_delta_mph_;
  }
  target_speed_mph_ = fmin(max_speed_mph_, target_speed_mph_);
  target_speed_mph_ = fmax(min_speed_mph_, target_speed_mph_);
 }

 void SetCrossTrackError(double cte)
 {
  current_cte_ = cte;
 }

 void SetTelemetrySpeed(double speed_mph)
 {
  current_speed_mph_ = speed_mph;
 }

 double Steer() const
 {
  return steering_controller_.Actuate();
 }

 double Throttle() const
 {
  return throttle_controller_.Actuate();
 }

private:
 // telemetry
 double current_speed_mph_{0.0F};
 double current_cte_{0.0F};

 // controllers
 PID throttle_controller_;
 PID steering_controller_;

 // target
 double max_throttle_{0.6};
 double min_throttle_{-0.6};

 double speed_delta_mph_{0.5}; // to avoid big jumps in speed
 double target_speed_mph_;
 double max_speed_mph_{30.0};
 double min_speed_mph_{20.0};
};

#endif // CAR_CONTROLLER_H
