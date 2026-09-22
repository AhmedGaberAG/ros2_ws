#!/usr/bin/env python3

import time
import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from std_msgs.msg import String

class SimpleLifecycleNode(LifecycleNode):
    def __init__(self):
        super().__init__("simple_lifecycle_node")
        self.get_logger().info("IN constructor")
        self.sub_ = None

    # Create ROS2 communications, connect to HW
    def on_configure(self, previous_state: LifecycleState):
        self.sub_ = self.create_subscription(
            String,
            "chatter",
            self.msgCallback,
            10
        )
        self.get_logger().info("Lifecycle node on_configure() called.")
        return TransitionCallbackReturn.SUCCESS

    # Activate / Enable HW
    def on_activate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_activate")
        time.sleep(2)
        return super().on_activate(previous_state)

    # Deactivate / Disable HW
    def on_deactivate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_deactivate")
        return super().on_deactivate(previous_state)
    
    # Destroy ROS2 communications, disconnect from HW
    def on_cleanup(self, previous_state: LifecycleState):
        self.destroy_subscription(self.sub_)
        self.get_logger().info("Lifecycle node on_cleanup() called.")
        return TransitionCallbackReturn.SUCCESS

    # Cleanup everything
    def on_shutdown(self, previous_state: LifecycleState):
        self.destroy_subscription(self.sub_)
        self.get_logger().info("Lifecycle node on_shutdown() called.")
        return TransitionCallbackReturn.SUCCESS

    # Process errors, deactivate + cleanup
    def on_error(self, previous_state: LifecycleState):
        self.destroy_subscription(self.sub_)

        self.get_logger().info("Lifecycle node on_error() called.")
        # do some checks, if ok, then return SUCESS, if not FAILURE
        return TransitionCallbackReturn.SUCCESS

    def msgCallback(self, msg):
        current_state = self._state_machine.current_state
        if current_state[1] == "active":
            self.get_logger().info(f"I heard: {msg.data}")

def main():
    rclpy.init()
    executor = rclpy.executors.SingleThreadedExecutor()
    simple_lifecycle_node = SimpleLifecycleNode()
    executor.add_node(simple_lifecycle_node)
    try:
        executor.spin()
    except (KeyboardInterrupt, rclpy.executors.ExternalShutdownException):
        simple_lifecycle_node.destroy_node()

if __name__ == "__main__":
    main()