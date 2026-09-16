#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class SmartPhone(Node):
    def __init__(self):
        super().__init__("smart_phone")
        self.subscriber_ = self.create_subscription(
            String,
            "robot_news",
            self.robotNewsCallback,
            10
        )
        self.get_logger().info("Smart Phone node initialized and subscribed to" \
                                " 'robot_news' topic.")
        
    def robotNewsCallback(self, msg):
        self.get_logger().info("Received news from robot: %s" % msg.data)

def main(args=None):
    rclpy.init(args=args)
    smart_phone = SmartPhone()
    rclpy.spin(smart_phone)
    smart_phone.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()