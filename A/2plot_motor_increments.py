import matplotlib.pyplot as plt
from lego_robot import LegoLogfile

if __name__ == "__main__":
    # Create an instance of LegoLogfile
    logfile = LegoLogfile()
    # Read motor data from the logfile
    logfile.read("robot4_motors.txt")

    # Print the first 40 entries of motor ticks
    for i in range(40):
        print(logfile.motor_ticks[i])

    # Plot the motor ticks
    plt.plot(logfile.motor_ticks)
    # Display the plot
    plt.show()
