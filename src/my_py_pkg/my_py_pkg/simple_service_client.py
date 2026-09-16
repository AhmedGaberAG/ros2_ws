#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
from functools import partial
import sys

class SimpleServiceClient(Node):

    def __init__(self, a, b):
        super().__init__("simple_service_client")

        self.client_ = self.create_client(
            AddTwoInts,
            "add_two_ints"
        )

        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn(
                "Service not available, waiting again..."
            )

        self.request_ = AddTwoInts.Request()
        self.request_.a = a
        self.request_.b = b

        self.future_ = self.client_.call_async(self.request_)

        self.future_.add_done_callback(
            partial(
                self.responseCallback,
                a=a,
                b=b
            )
        )

    def responseCallback(self, future, a, b):
        try:
            response = future.result()

            self.get_logger().info(
                str(a) + " + " +
                str(b) + " = " +
                str(response.sum)
            )

        except Exception as e:
            self.get_logger().error(
                "Service call failed %r" % (e,)
            )


def main(args=None):

    rclpy.init(args=args)

    if len(sys.argv) != 3:
        print(
            "wrong number of arguments! "
            "Usage: simple_service_client A B"
        )
        return -1

    add_two_ints = SimpleServiceClient(
        int(sys.argv[1]),
        int(sys.argv[2])
    )

    rclpy.spin(add_two_ints)

    add_two_ints.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()