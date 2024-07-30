import pygame
from jetracer.nvidia_racecar import NvidiaRacecar
import threading
import time

class JoystickController:
    def __init__(self, throttle_gain=0.2, steering_offset=0.1, joystick_index=0):
        # Initialize pygame
        pygame.init()

        # Initialize the joystick
        if pygame.joystick.get_count() < 1:
            raise Exception("No joystick connected")
        
        self.joystick = pygame.joystick.Joystick(joystick_index)
        self.joystick.init()

        # Initialize the racecar
        self.car = NvidiaRacecar()
        self.car.throttle_gain = throttle_gain
        self.car.steering_offset = steering_offset
        self.car.steering = 0

        print("Joystick and car are initialized!")

        self.running = False
        self.thread = None
    def map_value(self, value, in_min, in_max, out_min, out_max):
        # Map the joystick input value to the desired output range
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def update(self):
        # Pump the event queue
        pygame.event.pump()

        # Get joystick values
        steering = self.joystick.get_axis(0)  # Assuming axis 0 is for steering
        throttle = self.joystick.get_axis(3)  # Assuming axis 3 is for throttle

        # Map throttle value to range [-0.6, 0.6]
        mapped_throttle = self.map_value(throttle, -1.0, 1.0, -0.3, 0.3)

        # Update car controls
        self.car.steering = -steering
        self.car.throttle = mapped_throttle

        # Print values for debugging
        print(f"Steering: {self.car.steering}, Throttle: {self.car.throttle}")

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        try:
            while self.running:
                self.update()
                time.sleep(0.1)
        except Exception as e:
            print(f"Error: {e}")
        finally:
            pygame.quit()
            print("Pygame quit successfully!")

    def stop(self):
        self.running = False
        if self.thread is not None:
            self.thread.join()
            self.thread = None
        print("Joystick control stopped.")

##########TELEOPERATIONS##############
# Import the JoystickController class from the joystick_control.py script
from joystick_control import JoystickController

# Create an instance of the JoystickController
controller = JoystickController()

# To update the car based on joystick input, call the update method
controller.start()


