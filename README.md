# yahboom_arm
Ros2 package for moving the joints of yahboom robotic arm

# Topics:
 arm_joints - (JointState) receives commands for each of the 6 arm joints
 
msg.effort determines if velocity (rad/s) or time is sent to the joints
0 (default) - joint will execute command in a fixed time given in msg.velocity (s)
1           - joint will execute command using msg.velocity (rad/s)

