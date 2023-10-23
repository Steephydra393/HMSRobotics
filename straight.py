# Python Gyro Straight Dedicated
from motor import SMART_BRAKE, velocity
import motor_pair, math
from hub import port, motion_sensor
import time

# Notes:
# 10.87in per 360 degrees

class MoveStraight:
    def __init__(self, pair, left_motor, right_motor, motor_types, wheel_type):
        self.left_motor = left_motor
        self.right_motor = right_motor
        if motor_types == 1:
            self.max_speed = 660
            motor_pair.pair(pair, left_motor=left_motor, right_motor=right_motor)
            self.wheel_type = wheel_type
        elif motor_types == 2:
            self.max_speed = 1110
            motor_pair.pair(pair, left_motor=left_motor, right_motor=right_motor)
            self.wheel_type = wheel_type
        elif motor_types == 3:
            self.max_speed = 1050
            motor_pair.pair(pair, left_motor, right_motor)
            self.wheel_type = wheel_type
    
    def _correct_speed(self, yaw, re, retry=False):

        # Calculate the amount to adjust the motor speeds.
        correction = re - yaw

        # Set the motor speeds to the adjusted values.
        motor_pair.move_tank(
            motor_pair.PAIR_1, self.max_speed - correction, self.max_speed + correction
        )

        # Wait for the robot to turn to the desired angle.
        while motion_sensor.tilt_angles()[0] != re:
            pass

        # Stop the motors.
        motor_pair.stop(motor_pair.PAIR_1, stop=SMART_BRAKE)

        # Check if the robot is facing the desired angle.
        if motion_sensor.tilt_angles()[0] == re:
            print("Corrected, continuing...")

        # If the robot is not facing the desired angle, try again if possible.
        elif motion_sensor.tilt_angles()[0] >= re + 2 and motion_sensor.tilt_angles()[0] <= re - 2 and not retry:
            print("Huston, we have a problem, rerunning...")
            self._correct_speed(motion_sensor.tilt_angles()[0], re, retry=True)

        # Otherwise, give up.
        else:
            print("Huston, we have a problem... And We Can't Fix It...")

    def move_straight(self, inches, frequency):

        # Calculate the time to travel the specified distance at the given frequency.
        e = self.max_speed / 360
        ins = e * 10.87
        timen = inches / ins
        times = timen / frequency

        # Reset the gyro yaw angle.
        motion_sensor.reset_yaw(0)

        # Start moving the robot.
        motor_pair.move_tank(
            motor_pair.PAIR_1, self.max_speed, self.max_speed, acceleration=10000
        )

        # Start a timer.
        start_time = time.time()

        # Keep moving the robot until the specified time has elapsed.
        while time.time() - start_time < times:
            pass

        # Stop the robot.
        motor_pair.stop(motor_pair.PAIR_1, stop=SMART_BRAKE)

        # Correct the robot's final position if necessary.
        yaw = motion_sensor.tilt_angles()[0]
        if not math.isclose(yaw, 0, rel_tol=0.01):
            self._correct_speed(yaw, 0)
