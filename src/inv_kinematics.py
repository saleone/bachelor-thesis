#!/usr/bin/env python3
import math

def get_angles(x, y, z):
    """Return joint angles based on passed position."""

    # Values below are given in milimeters
    b = 35 # Shoulder width
    l1 = 120 # Shoulder to elbow length
    l2 = 100 # elbow to hand length

    # Shoulder to hand length
    d = math.sqrt(x ** 2 + y ** 2)

    # Hand from shoulder offset on z axis
    z_ = z - b

    # Helper
    cosineTheta2 = (d ** 2 + z_ ** 2 - l1 ** 2 - l2 ** 2) / 2 / l1 / l2

    # Shoulder rotation
    theta0 = math.atan2(y, x)

    # Lift of the arm in the shoulder
    theta2 = math.atan2(math.sqrt(1 - (cosineTheta2) ** 2), cosineTheta2)

    # Elbow rotation
    theta1 = math.atan2(z_, d) - \
        math.atan2(l2 * math.sin(theta2), l1 + l2 * math.cos(theta2))

    # Round values to specific angles
    result = []
    for value in [theta0, theta1, theta2]:
        # Convert from radians to degrees
        value = round(math.degrees(value))

        # If negative value then angle is in 3rd and 4th quandrant, transform
        # the value to apsolute angle value
        if value < 0:
            value = 360 + value

        result.append(value)

    return result

if __name__ == '__main__':
    from server import main
    main()