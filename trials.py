from hub import button, port, motion_sensor
import motor_pair, time

while True:
    if button.pressed(button.LEFT):
        print("Left button pressed")

        print("Performing slope test...")
        
        motor_pair.pair(motor_pair.PAIR_1, port.A, port.E)
        # (pair: int, degrees: int, steering: int, *, velocity: int = 360, stop: int = motor.BRAKE, acceleration: int = 1000, deceleration: int = 1000)
        motor_pair.move_for_degrees(motor_pair.PAIR_1, 1000, 0, velocity=580, stop=motor_pair.HOLD, acceleration=10000, deceleration=10000)
        velocity = 580
        step = 10
        time.sleep(.5)
        while true:
            velocity = velocity - step
            # (pair: int, steering: int, *, velocity: int = 360, acceleration: int = 1000)
            motor_pair.move(motor_pair.PAIR_1, 0, velocity=velocity, acceleration=10000)
            time.sleep(0.5)
            if velocity == 25:
                break
        
        time.sleep_ms(500)
        if motion_sensor.angular_velocity() == [0.0, 0.0, 0.0]:
            print("Slope test passed")
            print("Angular velocity: " + str(motion_sensor.angular_velocity()))

        elif motion_sensor.angular_velocity() == [0, 0, 0]:
            print("Slope test passed")
            print("Angular velocity: " + str(motion_sensor.angular_velocity()))

        elif motion_sensor.angular_velocity()[0] == 0 and motion_sensor.angular_velocity()[1] == 0 and motion_sensor.angular_velocity()[2] == 0:
            print("Slope test passed")
            print("Angular velocity: " + str(motion_sensor.angular_velocity()))

        else:
            print("Slope test failed, all conditions checked")
            print("Angular velocity: " + str(motion_sensor.angular_velocity()))
            motor_pair.stop(motor_pair.PAIR_1, stop=motor_pair.HOLD)
        

    elif button.pressed(button.RIGHT):
        print("Right button pressed")

        print("Sorry, no tests are available for this button.")
        # tests

        break

    else:
        pass