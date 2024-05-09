import matplotlib.pyplot as plt
from lego_robot import LegoLogfile

# Create an instance of LegoLogfile
logfile = LegoLogfile()

# Read the scan data from the logfile
logfile.read("robot4_scan.txt")

# Plot one scan
plt.plot(logfile.scan_data[8], label="Scan Data")  # Plot scan data
plt.title("Lego Scan Data")  # Add title
plt.xlabel("Scan Angle")  # Add x-axis label
plt.ylabel("Index")  # Add y-axis label
plt.legend()  # Add legend
plt.show()
