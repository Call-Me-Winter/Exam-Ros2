#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import String, Float32
from geometry_msgs.msg import Twist
from sensor_msgs.msg import JointState

class RobotController(Node):
    def __init__(self):
        super().__init__('robot_controller')
        self.status_pub = self.create_publisher(String, '/robot_status', 10)
        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.joint_pub = self.create_publisher(JointState, '/joint_states', 10)

        self.battery_sub = self.create_subscription(Float32, '/battery_level', self.battery_callback, 10)
        self.distance_sub = self.create_subscription(Float32, '/distance', self.distance_callback, 10)

        self.timer = self.create_timer(0.1, self.control_loop)  # 10 Hz
        self.battery = 100.0
        self.distance = 5.0
        self.wheel_pos = 0.0

    def battery_callback(self, msg):
        self.battery = msg.data

    def distance_callback(self, msg):
        self.distance = msg.data

    def control_loop(self):
        # Определяем статус
        status_msg = String()
        if self.battery < 20:
            status_msg.data = 'LOW BATTERY'
        elif self.distance < 1.0:
            status_msg.data = 'OBSTACLE NEAR'
        else:
            status_msg.data = 'NORMAL'
        self.status_pub.publish(status_msg)

        # Вычисляем команду скорости
        twist = Twist()
        if self.battery < 20:
            twist.linear.x = 0.0  # остановка
        elif self.distance < 1.0:
            twist.angular.z = 0.5  # поворот
        else:
            twist.linear.x = 0.2   # движение вперёд
        self.cmd_pub.publish(twist)

        # Публикация joint_states (для визуализации движения)
        js = JointState()
        js.header.stamp = self.get_clock().now().to_msg()
        js.name = ['base_to_left_wheel', 'base_to_right_wheel']
        self.wheel_pos += twist.linear.x * 0.1  # имитация вращения
        js.position = [self.wheel_pos, self.wheel_pos]
        self.joint_pub.publish(js)

def main(args=None):
    rclpy.init(args=args)
    node = RobotController()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()