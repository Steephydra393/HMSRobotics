# Python Gyro Straight Dedicated
try:
    from motor import SMART_BRAKE, velocity
    import motor_pair, math
    from hub import port, motion_sensor
    import time
except ImportError as e:
    print("Hmm, There was an error importing a module. Please make sure you have all the modules installed.\n" + str(e))
    raise Exception(SystemExit) # Exit the code.

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
        if yaw != re:
            motor.run(self.left_motor, 1050, acceleration=10000) # Adjust Acceleration *
            motor.run(self.right_motor, 1050, acceleration=10000) # Adjust Acceleration *
            while yaw != re:
                pass
            motor.stop(self.left_motor, stop=motor.SMART_BRAKE) # Stops the robot and adjusts for inaccuracy * Change if needed
            motor.stop(self.right_motor, stop=motor.SMART_BRAKE) # Stops the robot and adjusts for inaccuracy * Change if needed
            if motion_sensor.tilt_angles()[0] == r: # Best case scenario
                print("Corrected, continuing...")
            
            elif motion_sensor.tilt_angles()[0] >= r+2 and motion_sensor.tilt_angles()[0] <= r-2 and retry == False: # Possibly fixable
                print("Hustion, we have a problem, rerunning...")
                self._correct_speed(motion_sensor.tilt_angles()[0], re, retry=True)
            
            else: # Not fixable
                print("Huston, we have a problem... And We Can't Fix It...")
            
        else: # No clue what i was doing here, if this happens, yeaaa, we aint winning
            print("Huston, we have a problem...")

    def move_straight(self, inches, frequency, distance_per_rotation = 10.87, speed_degrees_per_second = 1030):
        if EXPERIMENTAL == True:
            print("* EXPERIMENTAL method 1 *")
            # Calculations:
            try:
                speed_inches_per_second = (speed_degrees_per_second / 360) * distance_per_rotation
                time_seconds = inches / speed_inches_per_second
                print("Time to travel " + str(inches) + " inches: " + str(time_seconds) + " seconds ✓")
                sleep_time = time_seconds / frequency # Figure out how many seconds it needs to sleep per cycle
                print("sleep time: " + str(sleep_time) + " seconds ✓")
            
            except MemoryError as e: # error handling
                print("𝕏 There was a memory error, please try again.\n" + str(e))
                raise Exception(SystemExit)
            except NameError as e: # error handling
                print("𝕏 There was a variable error, please try again.\n" + str(e))
                raise Exception(SystemExit)
            except Exception as e: # error handling
                print("𝕏 Hmm, there was an issue with the code, please try again.\n" + str(e))
                raise Exception(SystemExit)

            # Code:
            motion_sensor.reset_yaw(0) # reset the yaw to perfect 0
            e = 1
            elapsed_time = "N/A"
            print("Asuming trial 1 did fail...")
            while e <= frequency: # CYCLER

                start_time = time.time() # MAKE SURE NO CODE IS BEFORE THIS

                print(str(elapsed_time) + " it took to run past trial") # debug (REMOVE FROM COMP VERSION)
                print("Trial " + str(e) + " running...") # debug (REMOVE FROM COMP VERSION)
                correction = 0 - motion_sensor.tilt_angles()[0] # calculate the correction
                motor_pair.move_tank(motor_pair.PAIR_1, speed_degrees_per_second-correction, speed_degrees_per_second+correction, acceleration=10000) # add the correction to the speed
                e+=1 # add one to the cycle counter
                end_time = time.time()

                elapsed_time = end_time - start_time # MAKE SURE NO CODE IS PAST THIS

                time.sleep(time_seconds-elapsed_time) # sleep for the rest of the time
            
            if math.isclose(motion_sensor.tilt_angles()[0], 0):
                print("Congratts! Its acurate!")
            else:
                print("bruh its not good, fix it")
                self._correct_speed(motion_sensor.tilt_angles()[0], 0) # Try to fix it
        
        elif EXPERIMENTAL == 2:
            print("* EXPERIMENTAL method 2 *")
            # Calculations:

        else:
            print("WARNING, THIS CODE IS IN A NOT WORKING CONDITION, PLEASE USE THE EXPERIMENTAL BRANCH")
            print("max speed is " + str(self.max_speed))
            print("wheel type is " + str(self.wheel_type))
            te = 0
            ins = 0
            if self.wheel_type == 0:
                print("In/Second = unknown")
            else:
                e = self.max_speed/360
                print("In/Sec = " + str(e*10.87))
                ins = e*10.87
            timen = inches / ins
            print(timen) # debug
            times = timen/frequency
            motion_sensor.reset_yaw(0)
            while True:
                correction = 0 - motion_sensor.tilt_angles()[0]
                # print(correction) # debug
                motor_pair.move_tank(motor_pair.PAIR_1, self.max_speed-correction, self.max_speed+correction, acceleration=10000)
                # print(self.max_speed+correction, self.max_speed-correction) # debug
                time.sleep(times) # wait a few seconds
                te = te + times
                print(te)
                if te >= timen:
                    # print("...") # debug
                    motor_pair.stop(motor_pair.PAIR_1, stop=SMART_BRAKE)
                    break
                else:
                    # print("..") # debug
                    pass
            
            print("Completed first verse, correcting final position...")
            yaw = motion_sensor.tilt_angles()[0]
            if math.isclose(motion_sensor.tilt_angles()[0], 0): # allows for a 4 degree inconsistency
                print("It's acurate, finishing...")
            else:
                print("It's not acurate, fixing...") # how to fix
                self._correct_speed(yaw, 0)
