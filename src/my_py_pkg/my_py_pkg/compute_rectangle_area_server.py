#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.srv import ComputeRectangleArea

class ComputeRectangleAreaServer(Node):
    def __init__(self):
        super().__init__("compute_rectangle_area_server")
        self.services_ = self.create_service(
            ComputeRectangleArea, 
            "compute_rectangle_area",
            self.serviceCallback
            )
        self.get_logger().info("Service compute_rectangle_area is ready")

    def serviceCallback(self, request, response):
        response.area = request.width + request.length
        self.get_logger().info("Rectnagle Area Is : " + 
                               str(response.area))
        return response

def main(args=None):
    rclpy.init(args=args)
    compute_rectangle_area_server = ComputeRectangleAreaServer()
    rclpy.spin(compute_rectangle_area_server)
    compute_rectangle_area_server.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()