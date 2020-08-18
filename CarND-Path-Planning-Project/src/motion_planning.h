#ifndef SRC_MOTION_PLANNING_H_
#define SRC_MOTION_PLANNING_H_

#include <iostream>
#include <math.h>
#include <vector>

#include "json.hpp"

#include "helpers.h"
#include "vehicle.h"

#include "Spline/spline.h"

using std::vector;
using namespace std;

class MotionPlanner
{
public:
 Vehicle ego;
 vector<Vehicle> vehicles;
 int lane = 1;
 double ref_velocity = 0;

 json previous_path_x;
 json previous_path_y;
 // Previous path's end s and d values
 double end_path_s = 0.0;
 double end_path_d = 0.0;

 vector<double> map_waypoints_x_;
 vector<double> map_waypoints_y_;
 vector<double> map_waypoints_s_;
 vector<double> map_waypoints_dx_;
 vector<double> map_waypoints_dy_;

 MotionPlanner(vector<double> map_waypoints_x,
               vector<double> map_waypoints_y,
               vector<double> map_waypoints_s,
               vector<double> map_waypoints_dx,
               vector<double> map_waypoints_dy);

 void UpdateFusedRoadModel(json data);
 json Path();

 int GetFastestLane();
 double GetSafeDistance(double speed_mps);

 double LaneSpeed(int lane);
 double LaneCost(int lane);

 double DisplacementFromCenterLine(int lane);
 double WrappedDistance(double s1, double s2);
};

#endif /* SRC_MOTION_PLANNING_H_ */
