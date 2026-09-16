#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool
import sys


class NumberClient(Node):

    def __init__(self, data):
        super().__init__("number_client")

        self.client_ = self.create_client(
            SetBool,
            "reset_number_count"
        )

        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn(
                "Service not available, waiting again..."
            )

        self.request_ = SetBool.Request()
        self.request_.data = data

        self.future_ = self.client_.call_async(
            self.request_
        )

        self.future_.add_done_callback(
            self.responseCallback
        )

    def responseCallback(self, future):

        try:
            response = future.result()

            self.get_logger().info(
                f"Success: {response.success}"
            )

            self.get_logger().info(
                f"Message: {response.message}"
            )

        except Exception as e:
            self.get_logger().error(
                f"Service call failed: {e}"
            )


def main(args=None):

    rclpy.init(args=args)

    if len(sys.argv) != 2:
        print(
            "Wrong number of arguments!\n"
            "Usage: number_client [True or False]"
        )
        return -1

    data = sys.argv[1].lower() == "true"

    number_client = NumberClient(data)

    rclpy.spin(number_client)

    number_client.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()