#include "vehicle.h"
#include "config.h"
#include "helpers.h"

#include "math.h"

Vehicle::Vehicle()
{
}

Vehicle::Vehicle(json &j, bool isEgo)
{
 if (isEgo)
 {
  x = j[1]["x"];
  y = j[1]["y"];
  s = j[1]["s"];
  d = j[1]["d"];
  yaw_deg = j[1]["yaw"];
  yaw_rad = deg2rad(yaw_deg);

  speed = milesPerHourToMetersPerSecond(j[1]["speed"]);
 }
 else
 {
  id = j[0];
  x = j[1];
  y = j[2];
  vx = j[3];
  vy = j[4];
  s = j[5];
  d = j[6];

  lane = (int)(d / LANE_WIDTH);

  // Calculate yaw for non-ego cars (not necessarily required).

  yaw_deg = 0.0;
  yaw_rad = 0.0;

  // Deal with cases where vehicles does not follow s, but follows d
  //
  speed = sqrt(vx * vx + vy * vy);
 }

 lane = (int)(d / LANE_WIDTH);
}

void Vehicle::fillNextTickPositions(std::vector<double> &x, std::vector<double> &y, const int count)
{
}
