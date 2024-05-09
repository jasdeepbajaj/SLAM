import matplotlib.pyplot as plt
from lego_robot import LegoLogfile

def compute_derivative(scan, min_dist):
    jumps = [0]  # Initialize list for derivative values
    for i in range(1, len(scan) - 1):
        l = scan[i-1]
        r = scan[i+1]

        if l > min_dist and r > min_dist:
            # Compute derivative using central difference formula
            derivative = (r - l) / 2.0
            jumps.append(derivative)
        else:
            jumps.append(0)  # Set derivative to 0 if conditions not met

    jumps.append(0)
    return jumps

if __name__ == '__main__':
    minimum_valid_distance = 20.0

    # Read the scan data from the logfile
    logfile = LegoLogfile()
    logfile.read("robot4_scan.txt")

    scan_no = 8
    scan = logfile.scan_data[scan_no]

    # Compute derivative using provided function
    der = compute_derivative(scan, minimum_valid_distance)

    # Plot scan and derivative
    plt.plot(scan, label="Scan Data")  # Plot scan data
    plt.plot(der, label="Derivative")  # Plot derivative
    plt.title("Plot of scan %d" % scan_no)  # Add title
    plt.xlabel("Angle")  # Add x-axis label
    plt.ylabel("Value")  # Add y-axis label
    plt.legend()  # Add legend
    plt.grid(True)  # Add grid for better readability
    plt.show()
