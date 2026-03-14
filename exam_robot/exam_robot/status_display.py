#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class StatusDisplay(Node):
    def __init__(self):
        super().__init__('status_display')
        self.sub = self.create_subscription(String, '/robot_status', self.status_callback, 10)

    def status_callback(self, msg):
        self.get_logger().info(f'Robot status: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = StatusDisplay()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()