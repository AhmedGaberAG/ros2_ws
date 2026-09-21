#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from custom_interfaces.action import CountUntil
import sys

class CountUntilClient(Node):
    def __init__(self):
        super().__init__("count_until_client") 
        self.declare_parameter("frequency_to_cancel", 0.5)
        self.freq_to_cancel_ = self.get_parameter(
            "frequency_to_cancel"
        ).value

        self.count_until_client_ = ActionClient(
            self,
            CountUntil,
            "count_until"
        )

    def send_goal(self, target_number, period):
        # Wait for server
        self.count_until_client_.wait_for_server()

        # Create a goal
        goal = CountUntil.Goal()
        goal.target_number = target_number
        goal.period = period

        # Send a goal
        self.get_logger().info("Sending goal")

        future = self.count_until_client_.send_goal_async(
            goal,
            feedback_callback=self.goal_feedback_callback
        )

        future.add_done_callback(self.goal_response_callback)

        # Send a cancel request 2 seconds later
        # self.timer_ = self.create_timer(
        #     1 / self.freq_to_cancel_,
        #     self.cancel_goal
        # )

    def cancel_goal(self):
        self.get_logger().info("Sending a cancel request")
        self.goal_handle_.cancel_goal_async()
        self.timer_.cancel()

    def goal_response_callback(self, future):
        self.goal_handle_: ClientGoalHandle = future.result()

        if self.goal_handle_.accepted:
            self.get_logger().info("Goal got accepted")
            self.goal_handle_.get_result_async(). \
                add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().warn("Goal got rejected")

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        self.get_logger().info(f"Result: {result.reached_number}")

    def goal_feedback_callback(self, feedback_msg):
        number = feedback_msg.feedback.current_number
        self.get_logger().info(f"Got feedback: {number}")

def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 3:
        print(
            "Wrong number of arguments! "
            "Usage: count_until_client target_number period"
        )
        return -1
    
    count_until_client = CountUntilClient()
    count_until_client.send_goal(
        int(sys.argv[1]),
        float(sys.argv[2])
    )
    rclpy.spin(count_until_client)
    count_until_client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()