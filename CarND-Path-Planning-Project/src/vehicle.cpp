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
  yaw = j[1]["yaw"];
  yaw_rad = deg2rad(yaw);

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

  // TODO: Calculate yaw for non-ego cars (not necessarily required).

  yaw = 0.0;
  yaw_rad = 0.0;

  // TODO: deal with cases where vehicles does not follow s, but follows d
  //
  speed = sqrt(vx * vx + vy * vy);
 }

 lane = (int)(d / LANE_WIDTH);
}

void Vehicle::fillNextTickPositions(std::vector<double> &x, std::vector<double> &y, const int count)
{
}
