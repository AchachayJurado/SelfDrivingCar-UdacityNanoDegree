#ifndef VEHICLE_H
#define VEHICLE_H

#include "json.hpp"
#include <vector>

using json = nlohmann::json;

/**
 * @brief A class that holds the information about a given vehicle.
 *
 * Assumptions:
 * - All lanes are same width
 * - speed calculation can be derived from vx and vy (simply implemented)
 *
 */
class Vehicle
{

public:
 Vehicle();
 Vehicle(json &j, bool isEgo);

 double s;
 double d;
 double vx;
 double vy;
 double x;
 double y;
 double yaw_deg; // yaw in degrees
 double yaw_rad; // yaw in radians
 int id;

 int lane;     // Calculated by dividing distance/lane width
 double speed; // Calculated from vx and vy

 void fillNextTickPositions(std::vector<double> &x, std::vector<double> &y, const int count);
};

#endif // VEHICLE_H
