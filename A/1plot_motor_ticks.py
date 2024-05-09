import matplotlib.pyplot as plt

if __name__ == "__main__":
    # Open the file for reading
    with open("robot4_motors.txt", "r") as f:
        left_list = []
        right_list = []
        # Iterate through each line in the file
        for line in f:
            # Split the line into a list of strings based on whitespace
            line_split = line.split()
            # Extract the motor values and convert them to integers
            left_motor = int(line_split[2])
            right_motor = int(line_split[6])
            # Append the values to their respective lists
            left_list.append(left_motor)
            right_list.append(right_motor)

    # Plot the left and right motor values
    plt.plot(left_list, label="Left Motor")
    plt.plot(right_list, label="Right Motor")
    # Add labels and title
    plt.xlabel("Time")
    plt.ylabel("Motor Value")
    plt.title("Left and Right Motor Values Over Time")
    # Add legend
    plt.legend()
    # Display the plot
    plt.show()
