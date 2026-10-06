#!/usr/bin/env python3
#coding: utf-8
import smbus
import time
# V0.0.5

class Arm_Device(object):

    def __init__(self):
        self.addr = 0x15
        self.bus = smbus.SMBus(1)

    # Set the bus servo angle interface: array
    def Arm_serial_servo_write_rad(self, id, angle, time):
        pos = int(2000+2200*angle/3.1415)
        if pos < 200:
            pos = int(200)
        if pos > 3800:
            pos = int(3800)
        value_H = (pos >> 8) & 0xFF
        value_L = pos & 0xFF
            
        time_H = (time >> 8) & 0xFF
        time_L = time & 0xFF
            
        try:
            self.bus.write_i2c_block_data(self.addr, 0x10 + id, [value_H, value_L, time_H, time_L])
        except:
            print('Arm_serial_servo_write6 I2C error')
    
    # Set the bus servo angle interface: array
    def Arm_serial_servo_write6_rad(self, joints, time):
        if len(joints) !=6:
            return
        
        data = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(6):
            pos = int(2000+2200*joints[i]/3.1415)
            if pos < 200:
                pos = int(200)
            if pos > 3800:
                pos = int(3800)
            data[2*i] = int((pos >> 8) & 0xFF)
            data[2*i+1] = int(pos & 0xFF)
            
            timeArr = [(time >> 8) & 0xFF, time & 0xFF]
            s_id = 0x1d
            
        try:
            self.bus.write_i2c_block_data(self.addr, 0x1e, timeArr)
            self.bus.write_i2c_block_data(self.addr, s_id, data)
        except:
            print('Arm_serial_servo_write6 I2C error')
    

    # Read the bus servo angle, id: 1-250 return 0-180
    def Arm_serial_servo_read_rad(self, id):
        if id < 1 or id > 250:
            print("id must be 1 - 250")
            return None
        try:
            self.bus.write_byte_data(self.addr, 0x37, id)
            time.sleep(0.003)
            pos = self.bus.read_word_data(self.addr, 0x37)
        except:
            print('Arm_serial_servo_read_any I2C error')
            return None

        pos = (pos >> 8 & 0xff) | (pos << 8 & 0xff00)
        angle_rad = 3.1415*(pos-2000)/2200.0
        return angle_rad

    # Set the bus servo neutral offset with one key, move it to the neutral position after power-on, and then send the following function, id: 1-6 (set), 0 (restore initial)
    def Arm_serial_servo_write_offset_switch(self, id):
        try:
            if id > 0 and id < 7:
                self.bus.write_byte_data(self.addr, 0x1c, id)
            elif id == 0:
                self.bus.write_byte_data(self.addr, 0x1c, 0x00)
                time.sleep(.5)
        except:
            print('Arm_serial_servo_write_offset_switch I2C error')

    # Read the status of one-key setting of the bus servo's median offset, 0 means that the corresponding servo ID cannot be found, 1 means success, 2 means failure out of range
    def Arm_serial_servo_write_offset_state(self):
        try:
            self.bus.write_byte_data(self.addr, 0x1b, 0x01)
            time.sleep(.001)
            state = self.bus.read_byte_data(self.addr, 0x1b)
            return state
        except:
            print('Arm_serial_servo_write_offset_state I2C error')
        return None

    # Read the servo status, return 0xda normally, return 0x00 if no data is read, other values are servo error
    def Arm_ping_servo(self, id):
        data = int(id)
        if data > 0 and data <= 250:
            reg = 0x38
            self.bus.write_byte_data(self.addr, reg, data)
            time.sleep(.003)
            value = self.bus.read_byte_data(self.addr, reg)
            times = 0
            while value == 0 and times < 5:
                self.bus.write_byte_data(self.addr, reg, data)
                time.sleep(.003)
                value = self.bus.read_byte_data(self.addr, reg)
                times += 1
                if times >= 5:
                    return None
            return value
        else:
            return None

    # Read the hardware version number
    def Arm_get_hardversion(self):
        try:
            self.bus.write_byte_data(self.addr, 0x01, 0x01)
            time.sleep(.001)
            value = self.bus.read_byte_data(self.addr, 0x01)
        except:
            print('Arm_get_hardversion I2C error')
            return None
        version = str(0) + '.' + str(value)
        # print(version)
        return version

    # Torque switch 1: open torque 0: close torque (can be broken)
    def Arm_serial_set_torque(self, onoff):
        try:
            if onoff == 1:
                self.bus.write_byte_data(self.addr, 0x1A, 0x01)
            else:
                self.bus.write_byte_data(self.addr, 0x1A, 0x00)
        except:
            print('Arm_serial_set_torque I2C error')

    # Set the number of the bus servo
    def Arm_serial_set_id(self, id):
        try:
            self.bus.write_byte_data(self.addr, 0x18, id & 0xff)
        except:
            print('Arm_serial_set_id I2C error')

    # Set the current product color 1~6, the corresponding color of the RGB light is on
    def Arm_Product_Select(self, index):
        try:
            self.bus.write_byte_data(self.addr, 0x04, index & 0xff)
        except:
            print('Arm_Product_Select I2C error')


    # Set K1 key mode, 0: default mode 1: learning mode
    def Arm_Button_Mode(self, mode):
        try:
            self.bus.write_byte_data(self.addr, 0x03, mode & 0xff)
        except:
            print('Arm_Button_Mode I2C error')

    # Restart the driver board
    def Arm_reset(self):
        try:
            self.bus.write_byte_data(self.addr, 0x05, 0x01)
        except:
            print('Arm_reset I2C error')



