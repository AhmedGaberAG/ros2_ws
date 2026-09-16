# !/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class SimplePublisher(Node):
    def __init__(self):
        super().__init__("simple_publisher")
        self.publisher_ = self.create_publisher(String, "chatter", 10)

        self.counter_ = 0
        self.frequency_ = 1.0  # Frequency in Hz

        self.get_logger().info("Publishing messages at a frequency of %f Hz"
                                % self.frequency_)
        
        self.timer_ = self.create_timer(1.0 / self.frequency_, self.timerCallback)

    def timerCallback(self):
        msg = String()
        msg.data = "Hello, ROS 2! %d" % self.counter_
        self.publisher_.publish(msg)
        self.get_logger().info("Publishing: '%s'" % msg.data)
        self.counter_ += 1

def main():
    rclpy.init()
    simple_publisher = SimplePublisher()
    rclpy.spin(simple_publisher)
    simple_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()