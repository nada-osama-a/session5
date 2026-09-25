import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from std_msgs.msg import Float32
from std_msgs.msg import String  
import math
import random
import json  

class TestPublisher(Node):
    def __init__(self):
        super().__init__('test_publisher_node')

        self.publisher_ = self.create_publisher(Odometry, '/robot/odometry', 10)
        self.imu_publisher_ = self.create_publisher(Float32, '/robot/imu', 10)
        self.status_publisher_ = self.create_publisher(String, '/rover/status', 10) 
        
        self.odom_timer = self.create_timer(0.5, self.publish_odom)
        #self.imu_timer = self.create_timer(0.5, self.publish_random_heading)
        self.status_timer = self.create_timer(1.0, self.publish_json_status) 
        
        self.angle = 0.0

    def publish_odom(self):
        msg = Odometry()
        msg.pose.pose.position.x = 3.0 * math.cos(self.angle)
        msg.pose.pose.position.y = 3.0 * math.sin(self.angle)
        self.publisher_.publish(msg)
        # self.get_logger().info(f'Published -> X: {msg.pose.pose.position.x:.2f} | Y: {msg.pose.pose.position.y:.2f}')
        self.angle += 0.1

    #def publish_random_heading(self):
    #    msg = Float32()
    #    random_angle = random.uniform(0.0, 360.0)
    #    msg.data = random_angle
    #    self.imu_publisher_.publish(msg)
    #    # self.get_logger().info(f' Published Heading: {msg.data:.2f} degrees')

    def publish_json_status(self):
        payload = {
            "battery": round(random.uniform(50.0, 100.0), 1),
            "vel": round(random.uniform(0.0, 5.0), 2),
            "ang_vel": round(random.uniform(-1.5, 1.5), 2),
            
            "angle": round(random.uniform(0.0, 360.0), 2)
        }
        msg = String()
        msg.data = json.dumps(payload)
        self.status_publisher_.publish(msg)
        self.get_logger().info(f' Published JSON: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = TestPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()