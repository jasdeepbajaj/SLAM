# Unit A

This unit explores the navigation mechanics of a robot equipped with a 2D LIDAR scanner and two wheel encoders. Each wheel encoder counts the rotations of its respective wheel in ticks, which translate to a specific distance that the robot travels.

`NOTE: Differences in wheel rotation speeds cause the robot to turn.`

## Representing Robot Motion
The robot's movement can be categorized into two primary types:
1. Circular movement
2. Straight movement

To estimate the new position of the robot after moving, we calculate the distance using:

`distance = motor_ticks * ticks_to_distance_ratio`


`This ratio is calculated by moving the robot a known distance and then dividing the number of ticks by this distance.`

### Circular Movement

![movement image](./assets/circular_move.png)

Details:
* **c** is the pivot center around which the robot rotates.
* **R** is the circular path's radius.
* **w** represents the robot's width.
* **theta** is the heading angle.
* **p** marks the midpoint of the robot's width.
* **alpha** is the angle through which the robot turns.

Using the arc length formula, we compute the radius of the robot's path. The difference in ticks between the two wheel encoders helps us determine the rotation angle:

![alpha & R formula](assets/alpha_R.png)

We then find the pivot point's coordinates:

![center coordinates](assets/center.png)

And calculate the robot's new position:

![new state](assets/new_state.png)

---
### Straight Movement

![straight image](assets/straight.png)

When both wheels move equally, indicating no turns, the new position is straightforward:

![straight movement state](assets/straight_state.png)

---
## Scanner Data

At this point we still don't have a good trajectory of the robot

![robot trajectory](./assets/trajectory.png)

The actual trajectory of the robot is the red dotted trajectory while the green one is the computed trajectory using motor ticks. It is not sufficient to use only the motor ticks, we need to use scanner data to correct the trajectory. This is done by calculating the detected cylinders position and assign them to the nearest possible landmark in the given map. But first let's understand how the cylinders are detected.

![cylinders](assets/cylinders.png)

When the robot detects a sharp decrease (high -ve derivative) in distance from one measurement to the next, it considers this as a potential starting point of a cylindrical object. This suggests that the robot has encountered the near edge of a cylinder. As the robot continues to take measurements, it tracks this potential cylinder. If the subsequent measurements indicate stable or consistent distances that are greater than a minimum threshold, it implies the side of a cylinder.

If there is a sharp increase (high +ve derivative) in distance after a series of consistent measurements, the robot considers this as the end of the cylinder. This transition signifies that the robot has passed the cylinder, moving from the body of the cylinder back to open space.

Throughout this process, if the conditions of beginning, continuation, and end of a cylinder are met, the robot calculates the average position of these measurements to determine the central axis of the cylinder.

![derivative](assets/derivative.png)

but due to measurement errors we need to set a threshold to derivatives that will be considered as a left/right edge of a cylinder BUT there might be a situation where the laser scans hit two cylinders with no gap which will result in two consecutive left edges (or right edges) as follows:

![consecutive cylinders](assets/consecutive_cylinders.png)

In situations where two cylinders are positioned directly behind one another, it can be challenging for a robot to accurately detect the end of the first cylinder. This difficulty arises because the robot might not observe a significant change in distance, which usually marks the boundary between objects. As the second cylinder begins right where the first one ends, the distance measured by the robot remains consistent, appearing as though the first cylinder simply continues.

To address this issue, a practical solution has been implemented: the robot is programmed to disregard the first negative derivative (a mathematical representation of a decrease in distance) it encounters. Instead, it considers the start of the cylinder from the point marked by the second negative derivative. This approach helps in more accurately determining where one cylinder ends and the next begins, ensuring more reliable object detection by the robot.

![work around](assets/workaround.png)

After going through all these steps we end up with this trajectory (that could be improved) of our robot as follows:

![final trajectory](assets/final_trajectory.png)

