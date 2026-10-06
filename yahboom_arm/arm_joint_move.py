# !/usr/bin/env python
# coding: utf-8

import rclpy
from rclpy.node import Node
from rclpy import qos

import signal, os, time, math

from std_msgs.msg import Int32
from sensor_msgs.msg import JointState

from .Arm_Lib import Arm_Device


class ArmJointMove(Node):

    def __init__(self):
        super().__init__('arm_joint_move')
        
        self.Arm = Arm_Device()
        
        self.sub_joints = self.create_subscription(JointState,'arm_joints',self.arm_joints_callback,qos.qos_profile_sensor_data)
        self.sub_reset = self.create_subscription(Int32,'arm_reset',self.arm_reset_callback,qos.qos_profile_sensor_data)
        
        self.dt_joint_read = 0.05  # seconds
        self.timer = self.create_timer(self.dt_joint_read, self.pub_joints_callback)
        
        self.pub_joints = self.create_publisher(JointState, 'arm_joints_out', 10)
        
        self.position = [0,0,0,0,0,0]
        
        self.min = [-2.7, -1.57, -2.4, -2.2, -1.57, -1.57]
        self.max = [2.7, 1.57, 2.4, 2.2, 1.57, 1.57]
        self.offset = [0.0, 0.0, 0.0, 0.0, 0.785, 0.0]
        
        self.v_max = [3.14, 3.14, 3.14, 3.14, 3.14, 3.14]
        
        self.v = [1, 1, 1, 1, 1, 1]
        self.velocity_type = [0, 0, 0, 0, 0, 0]
        
        for i in range(6):
            ret = self.Arm.Arm_serial_servo_read_rad(i+1)
            if ret != None:
                self.position[i] = ret
        
    def arm_joints_callback(self,msg):
        if len(msg.velocity) == 6:
            for i in range(6):
                if msg.velocity[i]<self.v_max[i]:
                    self.v[i] = msg.velocity[i]
                else:
                    self.v[i] = self.v_max[i]
        
        # msg.effort determines if velocity (rad/s) or time is sent to the joints
        # 0 (default) - joint will execute command in a fixed time given in msg.velocity (s)
        # 1           - joint will execute command using msg.velocity (rad/s)
        if len(msg.effort) == 6:
            self.velocity_type = msg.effort
                
            
        if len(msg.position) == 6:
            for i in range(6):
                id = i+1
                angle = msg.position[i]
                
                if angle>self.max[i]:
                    angle = self.max[i]
                if angle<self.min[i]:
                    angle = self.min[i]
                
                d_angle = math.fabs(angle - self.position[i])
                
                # calculate dt according to velocity type (rad/s or s)
                if self.velocity_type[i] == 1:
                    dt = d_angle/self.v[i]*1000
                else:
                    dt = self.v[i]*1000
                
                self.Arm.Arm_serial_servo_write_rad(id, angle - self.offset[i], int(dt))
                time.sleep(.003)
                
    def pub_joints_callback(self):
        msg = JointState()
        msg.position = [0, 0, 0, 0, 0, 0]

        for i in range(6):
            ret = self.Arm.Arm_serial_servo_read_rad(i+1)
            if ret != None:
                msg.position[i] = ret + self.offset[i]
                self.position[i] = msg.position[i]
                
        #print(msg.position)
            
        self.pub_joints.publish(msg)

    def arm_reset_callback(self,msg):
        if msg.data == 1:
            self.Arm.Arm_reset()            
        
    def stop_handler(self,signum, frame):        
        rclpy.shutdown()


def main(args=None):
    rclpy.init(args=args)
    
    arm_joint_move = ArmJointMove()
    
    print("Arm joint move started")

    #signal.signal(signal.SIGINT, arm_joint_move.stop_handler)
    
    rclpy.spin(arm_joint_move)
    
    arm_joint_move.destroy_node()


if __name__ == '__main__':
    main()

