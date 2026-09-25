import json
from PySide6.QtCore import QObject, QThread, Signal
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from std_msgs.msg import String
#from sensor_msgs.msg import CompressedImage
from console.ros_nodes.joy_node import  JoyNode

class Signals(QObject):
    telemetry_signal = Signal(dict)
    #camera1 = Signal(CompressedImage)
    #camera2 = Signal(CompressedImage)

class WorkerNode(Node):
    def __init__(self, signals: Signals):
        super().__init__('worker_node')
        self.signals = signals
        
        self.latest_x = 0.0
        self.latest_y = 0.0 
        self.latest_angle = 0.0

        self.latest_battery = 0.0
        self.latest_vel = 0.0
        self.latest_ang_vel = 0.0

        self.create_subscription(Odometry, '/robot/odometry', self.odom_callback, 10)
        #self.create_subscription(Float32, '/robot/imu', self.imu_callback, 10)
        self.create_subscription(String, "/rover/status", self.status_callback, 10)
        
        self.create_timer(0.1, self.push_telemetry_to_gui)
        
    def odom_callback(self, msg: Odometry):
        self.latest_x = msg.pose.pose.position.x
        self.latest_y = msg.pose.pose.position.y

    #def imu_callback(self, msg: Float32):
    #    self.latest_angle = msg.data

    def status_callback(self, msg: String):
        received_data = json.loads(msg.data)
        
        if self.is_valid_payload(received_data):
            self.latest_battery = float(received_data["battery"])
            self.latest_vel = float(received_data["vel"])
            self.latest_ang_vel = float(received_data["ang_vel"])

            self.latest_angle = float(received_data["angle"])

            #self.get_logger().info(f"Received valid JSON: {received_data}")

            
        else:
            self.get_logger().warning(f"Received invalid JSON: {received_data}")
        
    def push_telemetry_to_gui(self):

        self.signals.telemetry_signal.emit({
            "x": self.latest_x,
            "y": self.latest_y,
            "angle": self.latest_angle,

            "battery": self.latest_battery,
            "vel": self.latest_vel,
            "ang_vel": self.latest_ang_vel
        })

    def is_valid_payload(self, data: dict) -> bool:
        required_keys = ["battery", "vel", "ang_vel", "angle"]
        for key in required_keys:
            if key not in data:
                return False
        
        if not isinstance(data["battery"], (int, float)): return False
        if not isinstance(data["vel"], (int, float)): return False
        if not isinstance(data["ang_vel"], (int, float)): return False
        if not isinstance(data["angle"], (int, float)): return False
        
        return True

class WorkerThread(QThread):
    def __init__(self, parent:QObject | None = None):
        super().__init__(parent)
        self.signals = Signals()
        self._node : WorkerNode | None = None
        self._joy_node : JoyNode | None = None
        
    def run(self):
        rclpy.init()
        self._node = WorkerNode(self.signals)
        self._joy_node = JoyNode()
        executor = SingleThreadedExecutor()
        executor.add_node(self._node)
        executor.add_node(self._joy_node)
        executor.spin()
        self._node.destroy_node()
        self._joy_node.destroy_node()
        rclpy.shutdown()
        