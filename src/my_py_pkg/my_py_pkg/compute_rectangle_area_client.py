#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.srv import ComputeRectangleArea
from functools import partial
import sys

class ComputeRectangleAreaClient(Node):
    def __init__(self, width, length):
        super().__init__("compute_rectangle_area_client")
        self.client_ = self.create_client(ComputeRectangleArea, "compute_rectangle_area")

        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn("Service not available, waiting again...")

        self.request_ = ComputeRectangleArea.Request()
        self.request_.width = width
        self.request_.length = length

        self.future_ = self.client_.call_async(self.request_)
        self.future_.add_done_callback(
            partial(
                self.responseCallback,
                width=width,
                length=length
            )
        )

    def responseCallback(self, future, width, length):
        try:
            response = future.result()
            self.get_logger().info("Rectnagle (width: %f, length: %f) Area Is : "
                                    % (width, length) + str(response.area))
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))

def main(args=None):
    rclpy.init(args=args)

    if len(sys.argv) != 3:
        print(
            "wrong number of arguments! "
            "Usage: compute_rectangle_area_client Width Length"
        )
        return -1

    compute_rectangle_area_client = ComputeRectangleAreaClient(
        float(sys.argv[1]),
        float(sys.argv[2])
    )
    rclpy.spin(compute_rectangle_area_client)
    compute_rectangle_area_client.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()