#!/usr/bin/env python3

import rclpy
from rclpy.lifecycle import LifecycleNode
from rclpy.lifecycle.node import LifecycleState, TransitionCallbackReturn
from std_msgs.msg import Int64

class NumberPublisherLifecycleNode(LifecycleNode):
    def __init__(self):
        super().__init__("number_publisher_life_cycle_node")
        self.get_logger().info("IN constructor")
        self.declare_parameter("number", 1)
        self.declare_parameter("frequency", 1.0)      
        self.number_ = self.get_parameter("number").value
        self.frequency_ = self.get_parameter("frequency").value
        self.publisher_ = None
        self.timer_ = None

    # Create ROS2 communications, connect to HW 
    def on_configure(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_configure")
        self.publisher_ = self.create_lifecycle_publisher(Int64, "number", 10)
        self.timer_ = self.create_timer(1.0 / self.frequency_, self.timerCallback)
        self.timer_.cancel()
        return TransitionCallbackReturn.SUCCESS # OR FAILURE OR ERROR

    # Activate/Enable HW
    def on_activate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_activate")
        self.timer_.reset()
        return super().on_activate(previous_state)

    # Deactivate/Disable HW
    def on_deactivate(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_adectivate")
        self.timer_.cancel()
        return super().on_deactivate(previous_state)
    
    # Destroy ROS2 communications, disconnect from HW 
    def on_cleanup(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_cleanup")
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_timer(self.timer_)
        return TransitionCallbackReturn.SUCCESS # OR FAILURE OR ERROR

    # Cleanup everything
    def on_shutdown(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_shutdown")
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_timer(self.timer_)
        return TransitionCallbackReturn.SUCCESS # OR FAILURE OR ERROR

    # Process errors, deactivate + cleanup
    def on_error(self, previous_state: LifecycleState):
        self.get_logger().info("IN on_error")
        self.destroy_lifecycle_publisher(self.publisher_)
        self.destroy_timer(self.timer_)
        # do some checks, if ok, then return SUCESS, if not FAILURE
        return TransitionCallbackReturn.SUCCESS # OR FAILURE
        
    def timerCallback(self):
        msg = Int64()
        msg.data = self.number_
        self.publisher_.publish(msg)
        self.number_ += 1
    
def main(args=None):
    rclpy.init(args=args)
    number_publisher_lifecycle_node = NumberPublisherLifecycleNode()
    rclpy.spin(number_publisher_lifecycle_node)
    number_publisher_lifecycle_node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()