#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class Node1(Node):
    def __init__(self):
        super().__init__("node1")
        self.timer = self.create_timer(1.0, self.callback)
    def callback(self):
        self.get_logger().info("Node 1 is running")