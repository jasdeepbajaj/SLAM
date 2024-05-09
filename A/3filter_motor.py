from math import sin, cos, pi
import matplotlib.pyplot as plt
from lego_robot import *

def filter_step(old_pose, motor_ticks, ticks_to_mm, robot_width):
    # This function computes the new position and orientation of the robot after moving.

    # Check if the robot has turned or not.
    if motor_ticks[0] == motor_ticks[1]:
        # If no turn, the robot moves straight.
        theta = old_pose[2]  # Current orientation
        x = old_pose[0] + motor_ticks[0] * ticks_to_mm * cos(theta)  # New x-coordinate
        y = old_pose[1] + motor_ticks[0] * ticks_to_mm * sin(theta)  # New y-coordinate
        return (x, y, theta)
    else:
        # If there is a turn, calculate the new pose.
        x = old_pose[0]
        y = old_pose[1]
        theta = old_pose[2]
        # Calculate the turning angle and radius.
        alpha = ticks_to_mm * (motor_ticks[1] - motor_ticks[0]) / robot_width
        R = motor_ticks[0] * ticks_to_mm / alpha
        # Compute the center of the turning circle.
        C = [x - (R + robot_width / 2) * sin(theta), y + (R + robot_width / 2) * cos(theta)]
        # Update the orientation
        theta += alpha
        theta = theta % (2 * pi)  # Normalize the angle
        # Calculate the new position.
        x = C[0] + (R + robot_width / 2) * sin(theta)
        y = C[1] - (R + robot_width / 2) * cos(theta)
        return (x, y, theta)

if __name__ == '__main__':
    ticks_to_mm = 0.349  # Conversion factor from encoder ticks to mm.
    robot_width = 150.0  # Width of the robot.

    # Read and parse the motor ticks from the log file.
    logfile = LegoLogfile()
    logfile.read("robot4_motors.txt")

    pose = (0.0, 0.0, 0.0)  # Initial robot pose (x, y, theta).
    filtered = []  # List to store the computed poses.

    # Process each set of motor ticks.
    for ticks in logfile.motor_ticks:
        pose = filter_step(pose, ticks, ticks_to_mm, robot_width)
        filtered.append(pose)

    # Plot the path of the robot.
    for pose in filtered:
        print(pose)
        plt.plot([p[0] for p in filtered], [p[1] for p in filtered], 'bo')
    plt.show()
