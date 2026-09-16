#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

counter = 0

def timer_callback():
    global counter
    counter += 1
    print(f"Timer callback executed {counter} times.")


def main(args=None):
    rclpy.init(args=args)
    node = Node("my_node")
    node.get_logger().info("Hello, ROS 2!")
    node.create_timer(1.0, timer_callback)
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()