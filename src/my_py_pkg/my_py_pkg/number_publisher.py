#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64

class NumberPublisher(Node):
    def __init__(self):
        super().__init__("number_publisher")
        self.publisher_ = self.create_publisher(Int64, "number", 10)

        self.frequency_ = 1.0  # Frequency in Hz
        self.number_ = 2

        self.get_logger().info("Publishing messages at a frequency of %f Hz"
                                % self.frequency_)
        self.timer_ = self.create_timer(1.0 / self.frequency_, self.timerCallback)

    def timerCallback(self):
        msg = Int64()
        msg.data = self.number_
        self.publisher_.publish(msg)
    
def main(args=None):
    rclpy.init(args=args)
    number_publisher = NumberPublisher()
    rclpy.spin(number_publisher)
    number_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()