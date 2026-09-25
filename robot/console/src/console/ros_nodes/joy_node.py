from rclpy.node import Node
from sensor_msgs.msg import Joy
from pynput import keyboard
import threading 

class JoyNode(Node):
    def __init__(self):
        super().__init__('joy_node')
        self.cmd_publisher = self.create_publisher(Joy, '/joy', 10)
        self._timer = self.create_timer(0.05, self.publish_joy_command)

        self.throttle = 0.0 
        self.steering = 0.0  
        self.gripper = 0    

        self.rlock = threading.RLock()
        
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()

    def on_press(self, key):
        with self.rlock:
            try:
                if key.char == 'w': self.throttle = 1.0
                elif key.char == 's': self.throttle = -1.0
                elif key.char == 'a': self.steering = 1.0   
                elif key.char == 'd': self.steering = -1.0  
                elif key.char == 'g': self.gripper = 1      
            except AttributeError:
                pass
                

    def on_release(self, key):
        with self.rlock:
            try:
                if key.char in ['w', 's']: self.throttle = 0.0
                elif key.char in ['a', 'd']: self.steering = 0.0
                elif key.char == 'g': self.gripper = 0      
            except AttributeError:
                pass

    def publish_joy_command(self):
        msg = Joy()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = "keyboard_joy"
        
        with self.rlock:
            msg.axes = [float(self.throttle), float(self.steering)] 
            msg.buttons = [int(self.gripper)]
        
        self.cmd_publisher.publish(msg)