# yahboom_arm
Ros2 package for moving the joints of yahboom robotic arm

### Topics:
* `arm_joints`: (JointState) receives commands for each of the 6 arm joints
* `arm_joints_out`: (JointState) publishes position for each of the 6 arm joints

The `arm_joints` topic needs to have 6 elements in the effort, velocity and position fields.
 
The `effort` field determines if velocity (rad/s) or time is sent to the joints
* 0 (default) - joint will execute command in a fixed time given in `velocity` field (s)
* 1           - joint will execute command using `velocity` field (rad/s)

The `position` field should have each joint position in radians. 
