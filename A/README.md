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

Using motor ticks alone is insufficient as shown by the discrepancy between the actual and estimated trajectories:
![robot trajectory](./assets/trajectory.png)

Scanner data helps refine our path by detecting cylinders (obstacles) and aligning them with known landmarks:
![cylinders](assets/cylinders.png)

Edges of each cylinder are identified by changes in the depth captured by the LIDAR:
![derivative](assets/derivative.png)

Challenges such as overlapping cylinders are addressed by averaging detections:
![consecutive cylinders](assets/consecutive_cylinders.png)
![work around](assets/workaround.png)

The processed data results in a refined approximation of the robot's trajectory:
![final trajectory](assets/final_trajectory.png)

