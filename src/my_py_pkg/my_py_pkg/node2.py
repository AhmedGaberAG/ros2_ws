#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class Node2(Node):
    def __init__(self):
        super().__init__("node2")
        self.timer = self.create_timer(2.0, self.callback)
    def callback(self):
        self.get_logger().info("Node 2 is running")
