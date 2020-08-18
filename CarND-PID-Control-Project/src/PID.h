#ifndef PID_H
#define PID_H

#include <chrono>
#include <cmath>

using Clock = std::chrono::system_clock;
using TimePoint = std::chrono::time_point<Clock>;

class PID
{
public:
  PID() { prev_time = Clock::now(); };

  /**
   * Initialize PID.
   * @param (Kp, Ki, Kd) The initial PID coefficients
   */
  void Init(double Kp, double Ki, double Kd)
  {
    Kp_ = Kp;
    Ki_ = Ki;
    Kd_ = Kd;
  }

  /**
   * Update the PID error variables given cross track error.
   * @param cte The current cross track error
   */
  void UpdateError(double cte)
  {
    double delta_time_s = GetDeltaTime();

    // Proportional
    p_error = cte;

    // Integral
    i_error += cte * delta_time_s;

    // Derivative
    d_error = (cte - prev_error_) / delta_time_s;

    // Save last values
    prev_error_ = cte;
    prev_time = Clock::now();
  }

  void SetLimits(double min, double max)
  {
    min_ = min;
    max_ = max;
  }

  double Actuate() const
  {
    // raw pid
    double action = Kp_ * p_error + Ki_ * i_error + Kd_ * d_error;

    // anti winding up ignores I when outside limits
    if (action < min_ or max_ < action)
    {
      action = Kp_ * p_error + Kd_ * d_error;
    }

    // action is always limited
    return fmax(min_, fmin(max_, action));
  }

private:
  double GetDeltaTime()
  {
    TimePoint now = Clock::now();
    std::chrono::duration<double> delta_time_s = now - prev_time;
    return delta_time_s.count();
  }
  /**
   * PID Errors
   */
  double p_error{0.0};
  double i_error{0.0};
  double d_error{0.0};

  /**
   * PID Coefficients
   */
  double Kp;
  double Ki;
  double Kd;

  double Kp_;
  double Ki_;
  double Kd_;

  double min_;
  double max_;

  double prev_error_{0.0};
  TimePoint prev_time;
};

#endif // PID_H
