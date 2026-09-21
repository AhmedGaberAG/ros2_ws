#!/usr/bin/env python3

import time
import threading
import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer
from rclpy.action.server import ServerGoalHandle, GoalResponse, CancelResponse
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
from custom_interfaces.action import MoveRobot

class MoveRobotServer(Node):

    def __init__(self):
        super().__init__("move_robot_server")
        self.declare_parameter("robot_position", 50)
        self.robot_position_ = self.get_parameter("robot_position").value

        self.goal_handle_: ServerGoalHandle = None
        self.goal_lock_ = threading.Lock()

        self.move_robot_server_ = ActionServer(
            self,
            MoveRobot,
            "move_robot",
            goal_callback=self.goal_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup()
        )

        self.get_logger().info("Move robot server started.")
        self.get_logger().info(f"Robot position: {self.robot_position_}")

    def goal_callback(self, goal_request: MoveRobot.Goal):
        self.get_logger().info("Received a new goal")

        # Validate goal
        if goal_request.position not in range(0, 100):
            self.get_logger().warn("Invalid position, reject goal")
            return GoalResponse.REJECT
        if goal_request.velocity <= 0:
            self.get_logger().warn("Invalid velocity, reject goal")
            return GoalResponse.REJECT
        
        # Preempt previous goal
        with self.goal_lock_:
            if self.goal_handle_ is not None:
                if self.goal_handle_.is_active:
                    self.get_logger().info("Preempting previous goal")
                    self.goal_handle_.abort()

        self.get_logger().info("Accept goal")
        return GoalResponse.ACCEPT

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Received a cancel request")
        return CancelResponse.ACCEPT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        # Store current goal
        with self.goal_lock_:
            self.goal_handle_ = goal_handle

        goal_position = goal_handle.request.position
        velocity = goal_handle.request.velocity

        self.get_logger().info(
            f"Executing goal: position={goal_position}, "
            f"velocity={velocity}"
        )

        result = MoveRobot.Result()
        feedback = MoveRobot.Feedback()

        while rclpy.ok():
            # Goal was aborted/preempted
            if not goal_handle.is_active:
                result.position = self.robot_position_
                result.message = "Preempted by another goal"
                return result

            # Cancel requested
            if goal_handle.is_cancel_requested:
                result.position = self.robot_position_
                if self.robot_position_ == goal_position:
                    result.message = "Success after cancel request"
                    goal_handle.succeed()
                else:
                    result.message = "Canceled"
                    goal_handle.canceled()
                return result

            # Calculate distance to target
            diff = goal_position - self.robot_position_

            # Goal reached
            if diff == 0:
                result.position = self.robot_position_
                result.message = "Success"
                goal_handle.succeed()
                return result

            # Move forward
            if diff > 0:
                step = min(velocity, diff)
                self.robot_position_ += step

            # Move backward
            else:
                step = min(velocity, abs(diff))
                self.robot_position_ -= step

            self.get_logger().info(f"Current position: {self.robot_position_}")
            feedback.current_position = self.robot_position_
            goal_handle.publish_feedback(feedback)
            time.sleep(1.0)

        return result

def main(args=None):
    rclpy.init(args=args)
    move_robot_server = MoveRobotServer()
    executor = MultiThreadedExecutor()
    executor.add_node(move_robot_server)
    try:
        executor.spin()
    finally:
        move_robot_server.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()