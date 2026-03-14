#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32

class BatteryNode(Node):
    def __init__(self):
        super().__init__('battery_node')
        self.pub = self.create_publisher(Float32, '/battery_level', 10)
        self.timer = self.create_timer(1.0, self.timer_callback)
        self.level = 100.0

    def timer_callback(self):
        msg = Float32()
        msg.data = self.level
        self.pub.publish(msg)
        self.level -= 0.1
        if self.level < 0:
            self.level = 100.0
        self.get_logger().info(f'Battery: {msg.data:.1f}%')

def main(args=None):
    rclpy.init(args=args)
    node = BatteryNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()