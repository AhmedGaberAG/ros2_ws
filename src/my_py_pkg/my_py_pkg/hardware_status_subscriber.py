#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.msg import HardwareStatus

class HardwareStatusSubscriber(Node):
    def __init__(self):
        super().__init__("hardware_status_subscriber")
        self.subscriber_ = self.create_subscription(HardwareStatus, "hardware_status",
                                                    self.msgCallback, 10)
        self.get_logger().info("")

    def msgCallback(self, msg):
        self.get_logger().info("Hardware Status are : ")
        self.get_logger().info("    - temp : " + str(msg.temperature))
        self.get_logger().info("    - motor : " + str(msg.are_motor_ready))
        self.get_logger().info("    - meesage : " + msg.debug_message)

def main(args=None):
    rclpy.init(args=args)
    hardware_status_subscriber= HardwareStatusSubscriber()
    rclpy.spin(hardware_status_subscriber)
    hardware_status_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()