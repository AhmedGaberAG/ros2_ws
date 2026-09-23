#!/usr/bin/env python3

import time
import threading
import rclpy
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup, MutuallyExclusiveCallbackGroup
from std_msgs.msg import String

class SimpleMultiThreadedExecutor(Node):
    def __init__(self):
        super().__init__("simple_multi_threaded_executor")

        # Callback groups
        self.lidar_group = ReentrantCallbackGroup()
        self.motor_stop_group = MutuallyExclusiveCallbackGroup()

        # 1. Timer: Read LiDAR
        self.lidar_timer = self.create_timer(0.5, self.lidar_callback, 
                                             callback_group=self.lidar_group)

        # 2. Timer: Control motors
        self.motor_timer = self.create_timer(1.0, self.motor_callback, 
                                             callback_group=self.motor_stop_group)
        
        # 3. Subscriber: Emergency stop
        self.stop_subscriber = self.create_subscription(
            String, 
            "/emergency_stop", 
            self.stop_callback, 
            10, 
            callback_group=self.motor_stop_group
        )

    def lidar_callback(self):
        thread_name = threading.current_thread().name
        self.get_logger().info(f"LiDAR START | Thread: {thread_name}")
        time.sleep(2)
        self.get_logger().info(f"LiDAR DONE | Thread: {thread_name}")

    def motor_callback(self):
        thread_name = threading.current_thread().name
        self.get_logger().info(f"Motor START | Thread: {thread_name}")
        time.sleep(2)
        self.get_logger().info(f"Motor DONE | Thread: {thread_name}")

    def stop_callback(self, msg):
        thread_name = threading.current_thread().name
        self.get_logger().warn(f"EMERGENCY STOP | Thread: {thread_name}")

def main(args=None):
    rclpy.init(args=args)
    simple_multi_threaded_executor = SimpleMultiThreadedExecutor()
    executor = MultiThreadedExecutor(num_threads=3)
    executor.add_node(simple_multi_threaded_executor)
    executor.spin()
    simple_multi_threaded_executor.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
