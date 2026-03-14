#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32
from geometry_msgs.msg import Twist

class DistanceSensor(Node):
    def __init__(self):
        super().__init__('distance_sensor')
        self.pub = self.create_publisher(Float32, '/distance', 10)
        self.sub = self.create_subscription(Twist, '/cmd_vel', self.cmd_callback, 10)
        self.timer = self.create_timer(0.5, self.timer_callback)
        self.distance = 5.0
        self.speed = 0.0

    def cmd_callback(self, msg):
        self.speed = msg.linear.x

    def timer_callback(self):
        # Имитация движения: при движении расстояние уменьшается
        self.distance -= self.speed * 0.1
        if self.distance < 0.5:
            self.distance = 5.0
        msg = Float32()
        msg.data = self.distance
        self.pub.publish(msg)
        self.get_logger().info(f'Distance: {msg.data:.2f} m')

def main(args=None):
    rclpy.init(args=args)
    node = DistanceSensor()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()