#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class NumberSubscriber(Node):
    def __init__ (self):
        super().__init__("number_subscriber")

        self.subscriber_ = self.create_subscription(
            Int64, 
            "number_counter", 
            self.msgCallback,
            10
        )
        self.get_logger().info("Subscribed to topic 'number_count'")

    def msgCallback(self, new_msg):
        self.get_logger().info("Received: %s" % new_msg.data)

def main(args=None):
    rclpy.init(args=args)
    number_subscriber = NumberSubscriber()
    rclpy.spin(number_subscriber)
    number_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()