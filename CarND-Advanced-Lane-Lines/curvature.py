import numpy as np
import numpy.polynomial.polynomial as poly

ym_per_pix = 20/720  # meters per pixel in y dimension
xm_per_pix = 3.7/700  # meters per pixel in x dimension
ploty = np.linspace(0, 719, num=720)
IMG_WIDTH_HLF = 640


def curvature(left_fit_cr, right_fit_cr):
    y_eval = np.max(ploty)

    # Calculate the new radii of curvature
    left_curverad = ((1 + (2*left_fit_cr[0]*y_eval*ym_per_pix +
                           left_fit_cr[1])**2)**1.5) / np.absolute(2*left_fit_cr[0])
    right_curverad = ((1 + (2*right_fit_cr[0]*y_eval*ym_per_pix +
                            right_fit_cr[1])**2)**1.5) / np.absolute(2*right_fit_cr[0])

    return left_curverad, right_curverad


def lanepos(left_fit, right_fit):
    y_eval = np.max(ploty)

    left_fit = np.flip(left_fit, 0)
    right_fit = np.flip(right_fit, 0)
    leftl = poly.polyval(y_eval, left_fit)
    rightl = poly.polyval(y_eval, right_fit)

    center_road = leftl+((rightl-leftl)/2)
    center_car = 660
    caroff = (center_car-center_road)*xm_per_pix

    return leftl, rightl, caroff
