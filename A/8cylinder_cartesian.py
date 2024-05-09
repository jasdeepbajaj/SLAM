from lego_robot import *  # Importing necessary modules
from math import sin, cos  # Importing trigonometric functions

# Find the derivative in scan data, ignoring invalid measurements.
def compute_derivative(scan, min_dist):
    # Create an array to store the derivative values, initialized with zero.
    jumps = [0]
    # Iterate over the scan data to compute the derivative, ignoring the first and last elements.
    for i in range(1, len(scan) - 1):
        l = scan[i - 1]
        r = scan[i + 1]
        # Only compute derivative if both neighbors are above the minimum distance.
        if l > min_dist and r > min_dist:
            derivative = (r - l) / 2.0
            jumps.append(derivative)
        else:
            jumps.append(0)
    # Append zero for the last element (boundary condition).
    jumps.append(0)
    return jumps

# Function to find cylinders in scan data
def find_cylinders(scan, scan_derivative, jump, min_dist):
    cylinder_list = []  # List to store cylinder positions
    on_cylinder = False  # Flag to indicate if currently on a cylinder
    sum_ray, sum_depth, rays = 0.0, 0.0, 0  # Variables to accumulate ray and depth data

    for i in range(len(scan_derivative)):
        # Check for a negative jump indicating the start of a cylinder.
        if scan_derivative[i] < -jump:
            # Start a new cylinder if not already started.
            if not on_cylinder:
                on_cylinder = True
            # Reset variables if another cylinder is detected without closing the previous one.
            else:
                sum_ray, sum_depth, rays = 0.0, 0.0, 0
        # Check for a positive jump indicating the end of a cylinder.
        elif scan_derivative[i] > jump and rays > 0:
            if on_cylinder:
                # Calculate the average position and depth for the cylinder.
                cylinder_list.append((sum_ray / rays, sum_depth / rays))
                sum_ray, sum_depth, rays = 0.0, 0.0, 0  # Reset variables
            on_cylinder = False  # Mark the end of the cylinder
        # Collect data if currently on a cylinder and the measurement is above the minimum distance.
        elif on_cylinder and scan[i] > min_dist:
            sum_ray += i  # Accumulate ray index
            sum_depth += scan[i]  # Accumulate depth
            rays += 1  # Increment the number of valid rays

    return cylinder_list  # Return the list of cylinder positions

# Function to convert cylinder positions to Cartesian coordinates
def compute_cartesian_coordinates(cylinders: list, cylinder_offset: float):
    result = []  # List to store Cartesian coordinates
    for c in cylinders:
        angle = LegoLogfile.beam_index_to_angle(c[0])  # Convert beam index to angle
        x = (c[1] + cylinder_offset) * cos(angle)  # Compute x-coordinate
        y = (c[1] + cylinder_offset) * sin(angle)  # Compute y-coordinate

        result.append((x, y))  # Append Cartesian coordinates to result list
    return result  # Return the list of Cartesian coordinates

if __name__ == '__main__':

    minimum_valid_distance = 20.0  # Minimum valid distance for a measurement
    depth_jump = 100.0  # Threshold for identifying cylinder edges
    cylinder_offset = 90.0  # Offset for cylinder detection

    logfile = LegoLogfile()
    logfile.read("robot4_scan.txt")  # Read scan data from file

    out_file = open("8cylinders.txt", "w")  # Open output file for writing
    for scan in logfile.scan_data:
        # Find cylinders.
        der = compute_derivative(scan, minimum_valid_distance)  # Compute derivative of scan data
        cylinders = find_cylinders(scan, der, depth_jump, minimum_valid_distance)  # Find cylinders
        cartesian_cylinders = compute_cartesian_coordinates(cylinders, cylinder_offset)  # Convert to Cartesian coordinates
        # Write to file.

        out_file.write("D C ")  # Write header
        for c in cartesian_cylinders:
            out_file.write("%.1f %.1f " % c)  # Write Cartesian coordinates to file
        out_file.write("\n")  # Write newline character
    out_file.close()  # Close output file
