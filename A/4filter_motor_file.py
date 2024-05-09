from math import sin, cos, pi
import matplotlib.pyplot as plt
from lego_robot import * 

# Define the function to update the robot's position based on the movement.
def filter_step(old_pose, motor_ticks, ticks_to_mm, robot_width, scanner_displacement):
    l = motor_ticks[0] * ticks_to_mm  # Convert left motor ticks to millimeters.
    r = motor_ticks[1] * ticks_to_mm  # Convert right motor ticks to millimeters.
    w = robot_width  # Width of the robot.

    # If the wheels moved the same distance, the robot moved straight.
    if l == r:
        theta = old_pose[2]  # Current orientation
        x = old_pose[0] + l * cos(theta)  # Update x-coordinate based on movement.
        y = old_pose[1] + l * sin(theta)  # Update y-coordinate based on movement.
        return (x, y, theta)
    else:
        alpha = (r - l) / w  # Calculate the turning angle.
        R = l / alpha  # Calculate the turning radius for the left wheel.

        # Calculate the old body coordinates from the scanner's position.
        x_lidar_old = old_pose[0]
        y_lidar_old = old_pose[1]
        theta_lidar_old = old_pose[2]

        theta_body_old = theta_lidar_old
        x_body_old = x_lidar_old - scanner_displacement * cos(theta_body_old)
        y_body_old = y_lidar_old - scanner_displacement * sin(theta_body_old)
        
        # Calculate the rotation center.
        c_x = x_body_old - (R + w/2) * sin(theta_body_old)
        c_y = y_body_old + (R + w/2) * cos(theta_body_old)

        theta_body_new = theta_body_old + alpha  # Update the orientation with the turning angle.
        theta_body_new = theta_body_new % (2 * pi)  # Normalize the angle.

        # Calculate the new body position post-rotation.
        x_body_new = c_x + (R + w / 2) * sin(theta_body_new)
        y_body_new = c_y - (R + w / 2) * cos(theta_body_new)

        # Re-calculate the scanner's position based on the new body coordinates.
        x_lidar_new = x_body_new + scanner_displacement * cos(theta_body_new)
        y_lidar_new = y_body_new + scanner_displacement * sin(theta_body_new)

        return (x_lidar_new, y_lidar_new, theta_body_new)

if __name__ == "__main__":
    # Constants and initial pose setup.
    scanner_displacement = 30.0  # Scanner displacement from the robot's center.
    ticks_to_mm = 0.349  # Conversion factor from encoder ticks to millimeters.
    robot_width = 173.0  # Width of the robot.
    pose = (1850.0, 1897.0, 213.0 / 180.0 * pi)  # Initial pose in the lidar frame.

    # Read motor tick data from a file.
    logfile = LegoLogfile()
    logfile.read("robot4_motors.txt")

    filtered = []
    # Process each tick record to update the robot's pose.
    for ticks in logfile.motor_ticks:
        pose = filter_step(pose, ticks, ticks_to_mm, robot_width, scanner_displacement)
        filtered.append(pose)

    # Plotting the robot's trajectory.
    for pose in filtered:
        plt.plot([p[0] for p in filtered], [p[1] for p in filtered], 'bo')
    plt.show()

    # Write all filtered positions to a file.
    with open("4poses_from_ticks.txt", "w") as f:
        for pose in filtered:
            print("F %f %f %f" % pose, file=f)
