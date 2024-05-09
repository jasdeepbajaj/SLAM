import matplotlib.pyplot as plt
from lego_robot import LegoLogfile

def compute_derivative(scan, min_dist):
    jumps = [0]  # Initialize list for derivative values
    for i in range(1, len(scan) - 1):
        l = scan[i - 1]
        r = scan[i + 1]
        if l > min_dist and r > min_dist:
            derivative = (r - l) / 2.0
            jumps.append(derivative)
        else:
            jumps.append(0)
    jumps.append(0)
    return jumps

def find_cylinders(scan, scan_derivative, jump, min_dist):
    cylinder_list = []
    on_cylinder = False
    sum_ray, sum_depth, rays = 0.0, 0.0, 0

    for i in range(len(scan_derivative)):
        if scan_derivative[i] < -jump:
            if not on_cylinder:
                on_cylinder = True
            else:
                sum_ray, sum_depth, rays = 0.0, 0.0, 0
        elif scan_derivative[i] > jump and rays > 0:
            if on_cylinder:
                cylinder_list.append((sum_ray / rays, sum_depth / rays))
                sum_ray, sum_depth, rays = 0.0, 0.0, 0
            on_cylinder = False
        elif on_cylinder and scan[i] > min_dist:
            sum_ray += i
            sum_depth += scan[i]
            rays += 1

    return cylinder_list

if __name__ == '__main__':
    minimum_valid_distance = 30.0
    depth_jump = 100.0

    # Read the logfile which contains all scans.
    logfile = LegoLogfile()
    logfile.read("robot4_scan.txt")

    # Pick one scan from the data.
    scan = logfile.scan_data[235]

    # Compute derivative and find cylinders.
    der = compute_derivative(scan, minimum_valid_distance)
    cylinders = find_cylinders(scan, der, depth_jump, minimum_valid_distance)

    # Plot the scan and mark detected cylinders.
    plt.plot(scan, label="Scan Data")  # Plot scan data
    plt.scatter([c[0] for c in cylinders], [c[1] for c in cylinders], c='r', s=200, label="Detected Cylinders")  # Mark detected cylinders
    plt.title("Cylinder Detection")  # Add title
    plt.xlabel("Angle")  # Add x-axis label
    plt.ylabel("Distance")  # Add y-axis label
    plt.legend()  # Add legend
    plt.grid(True)  # Add grid for better readability
    plt.show()
