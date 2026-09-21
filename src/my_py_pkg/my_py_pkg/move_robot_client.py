#!/usr/bin/env python3

import sys
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from rclpy.action.client import ClientGoalHandle, GoalStatus
from custom_interfaces.action import MoveRobot
from example_interfaces.msg import Empty

class MoveRobotClient(Node):

    def __init__(self):
        super().__init__("move_robot_client")
        self.goal_handle_: ClientGoalHandle = None

        self.move_robot_client_ = ActionClient(
            self,
            MoveRobot,
            "move_robot"
        )
        self.cancel_subscriber_ = self.create_subscription(
            Empty,
            "cancel_move",
            self.cancel_goal,
            10
        )

    def send_goal(self, position, velocity):
        self.move_robot_client_.wait_for_server()

        goal = MoveRobot.Goal()
        goal.position = position
        goal.velocity = velocity
        self.get_logger().info(
            f"Send goal with position {position} "
            f"and velocity {velocity}"
        )

        future = self.move_robot_client_.send_goal_async(
            goal,
            feedback_callback=self.goal_feedback_callback
        )
        future.add_done_callback(self.goal_response_callback)

    def cancel_goal(self, msg):
        if self.goal_handle_ is not None:
            self.get_logger().info("Sending a cancel request")
            self.goal_handle_.cancel_goal_async()
        else:
            self.get_logger().warn("No active goal to cancel")
            
    def goal_response_callback(self, future):
        self.goal_handle_: ClientGoalHandle = future.result()
        if self.goal_handle_.accepted:
            self.get_logger().info("Goal got accepted")
            result_future = self.goal_handle_.get_result_async()
            result_future.add_done_callback(self.goal_result_callback)
        else:
            self.get_logger().warn("Goal got rejected")
            self.goal_handle_ = None

    def goal_result_callback(self, future):
        status = future.result().status
        result = future.result().result
        if status == GoalStatus.STATUS_SUCCEEDED:
            self.get_logger().info("Success")
        elif status == GoalStatus.STATUS_ABORTED:
            self.get_logger().error("Aborted")
        elif status == GoalStatus.STATUS_CANCELED:
            self.get_logger().warn("Canceled")
        else:
            self.get_logger().warn(f"Unknown status: {status}")
        self.get_logger().info( f"Result: {result.position}")
        self.get_logger().info( f"Message: {result.message}")
        self.goal_handle_ = None

    def goal_feedback_callback(self, feedback_msg):
        current_position = feedback_msg.feedback.current_position
        self.get_logger().info(f"Got feedback: {current_position}")

def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) != 3:
        print(
            "Wrong number of arguments!\n"
            "Usage: move_robot_client position velocity"
        )
        return -1

    move_robot_client = MoveRobotClient()
    move_robot_client.send_goal(
        int(sys.argv[1]),
        int(sys.argv[2])
    )
    try:
        rclpy.spin(move_robot_client)
    finally:
        move_robot_client.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()