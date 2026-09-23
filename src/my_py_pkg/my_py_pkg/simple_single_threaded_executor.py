#!/usr/bin/env python3

import time
import rclpy
from rclpy.node import Node
from rclpy.executors import SingleThreadedExecutor
from std_msgs.msg import String

class SimpleSingleThreadedExecutor(Node):
    def __init__(self):
        super().__init__("simple_single_threaded_executor")

        # 1. Timer: Read LiDAR
        self.lidar_timer = self.create_timer(0.5, self.lidar_callback)

        # 2. Timer: Control motors
        self.motor_timer = self.create_timer(1.0, self.motor_callback)

        # 3. Subscriber: Emergency stop
        self.stop_subscriber = self.create_subscription(
            String, 
            "/emergency_stop", 
            self.stop_callback, 
            10
        )

    def lidar_callback(self):
        self.get_logger().info("LiDAR callback: reading sensor...")
        time.sleep(2)
        self.get_logger().info("LiDAR callback: DONE")

    def motor_callback(self):
        self.get_logger().info("Motor callback: controlling motors")

    def stop_callback(self, msg):
        self.get_logger().warn(f"EMERGENCY STOP: {msg.data}")

def main(args=None):
    rclpy.init(args=args)
    simple_single_threaded_executor = SimpleSingleThreadedExecutor()
    executor = SingleThreadedExecutor()
    executor.add_node(simple_single_threaded_executor)
    executor.spin()
    simple_single_threaded_executor.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
