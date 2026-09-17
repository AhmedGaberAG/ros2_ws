#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__("my_node")
        self.declare_parameter("counter", 0)
        self.declare_parameter("frequency", 1.0)  
        self.counter_ = self.get_parameter("counter").value
        self.frequency_ = self.get_parameter("frequency").value 

        self.create_timer(1.0 / self.frequency_, self.timer_callback)
        self.get_logger().info("Hello, ROS 2!")

    def timer_callback(self):
        self.counter_ += 1
        self.get_logger().info(
            f"Timer callback executed {self.counter_} times.")

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()