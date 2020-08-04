
#ifndef HELPERS_H
#define HELPERS_H

#include <math.h>
#include <string>
#include <vector>

using std::vector;

// For converting back and forth between radians and degrees.
constexpr double pi();

double deg2rad(double x);
double rad2deg(double x);
double distance(double x1, double y1, double x2, double y2);

double milesPerHourToMetersPerSecond(double milesPerHour);

int ClosestWaypoint(double x, double y, const vector<double> &maps_x,
                    const vector<double> &maps_y);

int NextWaypoint(double x, double y, double theta, const vector<double> &maps_x,
                 const vector<double> &maps_y);

// Transform from Cartesian x,y coordinates to Frenet s,d coordinates
vector<double> getFrenet(double x, double y, double theta,
                         const vector<double> &maps_x,
                         const vector<double> &maps_y);

// Transform from Frenet s,d coordinates to Cartesian x,y
vector<double> getXY(double s, double d, const vector<double> &maps_s,
                     const vector<double> &maps_x,
                     const vector<double> &maps_y);

// Checks if the SocketIO event has JSON data.
// If there is data the JSON object in string format will be returned,
//   else the empty string "" will be returned.
std::string hasData(std::string s);

#endif // HELPERS_H
