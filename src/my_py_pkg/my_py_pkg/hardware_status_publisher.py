#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.msg import HardwareStatus

class HardwareStatusPublisher(Node):
    def __init__(self):
        super().__init__("hardware_status_publisher")
        self.declare_parameter("frequency", 1.0)        
        self.frequency_ = self.get_parameter("frequency").value

        self.publisher_ = self.create_publisher(HardwareStatus, "hardware_status", 10)
        self.timer_ = self.create_timer(1.0 / self.frequency_, self.timerCallback)
        self.get_logger().info("Hardware status publisher has been started")

    def timerCallback(self):
        msg = HardwareStatus()
        msg.temperature = 66
        msg.are_motor_ready = True
        msg.debug_message = "Nothing special here"
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    hardware_status_publisher = HardwareStatusPublisher()
    rclpy.spin(hardware_status_publisher)
    hardware_status_publisher.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()