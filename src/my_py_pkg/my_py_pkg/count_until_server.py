#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from rclpy.action import ActionServer, GoalResponse, CancelResponse
from rclpy.action.server import ServerGoalHandle
from custom_interfaces.action import CountUntil
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup
import time
import threading

class CountUntilServer(Node):
    def __init__(self):
        super().__init__("count_until_server")

        self.goal_handle_: ServerGoalHandle = None
        self.goal_lock_ = threading.Lock()
        self.goal_queue_ = []

        self.count_until_server_ = ActionServer(
            self,
            CountUntil,
            "count_until",
            goal_callback=self.goal_callback,
            handle_accepted_callback=self.handle_accepted_callback,
            cancel_callback=self.cancel_callback,
            execute_callback=self.execute_callback,
            callback_group=ReentrantCallbackGroup()
        )

        self.get_logger().info("Action server started.")

    def goal_callback(self, goal_request: CountUntil.Goal):
        self.get_logger().info("Received a goal")

        # Policy: refuse new goal if current goal still active
        # with self.goal_lock_:
        #     if self.goal_handle_ is not None and self.goal_handle_.is_active:
        #         self.get_logger().info("A goal is already active, rejecting new goal")
        #         return GoalResponse.REJECT

        # Validate the goal request
        if goal_request.target_number <= 0:
            self.get_logger().info(
                "Goal rejected: target_number must be greater than 0."
            )
            return GoalResponse.REJECT

        # Policy: preempt existing goal when receiving new goal
        # with self.goal_lock_:
        #     if self.goal_handle_ is not None and self.goal_handle_.is_active:
        #         self.get_logger().info("A goal is already active, rejecting new goal")
        #         self.goal_handle_.abort()

        self.get_logger().info("Goal accepted.")
        return GoalResponse.ACCEPT

    def handle_accepted_callback(self, goal_handle: ServerGoalHandle):
        with self.goal_lock_:
            # If a goal is already running,
            # put the new goal into the queue.
            if self.goal_handle_ is not None:
                self.goal_queue_.append(goal_handle)
                self.get_logger().info(f"Goal queued. Queue size: {len(self.goal_queue_)}")
                return

            # Otherwise, start the goal immediately.
            self.goal_handle_ = goal_handle

        goal_handle.execute()

    def cancel_callback(self, goal_handle: ServerGoalHandle):
        self.get_logger().info("Received a cancel request")
        return CancelResponse.ACCEPT  # or REJECT

    def execute_callback(self, goal_handle: ServerGoalHandle):
        # with self.goal_lock_:
        #     self.goal_handle_ = goal_handle

        # Get request from the goal
        target_number = goal_handle.request.target_number
        period = goal_handle.request.period

        # Execute the action
        self.get_logger().info("Executing the goal")
        feedback = CountUntil.Feedback()
        result = CountUntil.Result()
        counter = 0

        for _ in range(target_number):
            if not goal_handle.is_active:
                result.reached_number = counter
                self.process_next_goal_in_queue()
                return result
            if goal_handle.is_cancel_requested:
                self.get_logger().info("Canceling the goal")
                goal_handle.canceled()
                result.reached_number = counter
                self.process_next_goal_in_queue()
                return result
            counter += 1
            self.get_logger().info(f"Current Number: {counter}")
            feedback.current_number = counter
            goal_handle.publish_feedback(feedback)
            time.sleep(period)

        # Once done, set goal final state
        goal_handle.succeed()

        # and send the result
        result.reached_number = counter
        self.get_logger().info(f"Goal completed. Reached number: {counter}")

        # Start next goal from queue
        self.process_next_goal_in_queue()

        return result

    def process_next_goal_in_queue(self):
        with self.goal_lock_:
            if len(self.goal_queue_) > 0:
                next_goal = self.goal_queue_.pop(0)
                self.goal_handle_ = next_goal
            else:
                self.goal_handle_ = None
                self.get_logger().info("No more goals in the queue.")
                return

        next_goal.execute()


def main(args=None):
    rclpy.init(args=args)
    count_until_server = CountUntilServer()
    rclpy.spin(count_until_server, MultiThreadedExecutor())
    count_until_server.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
