#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts

class SimpleServiceServer(Node):
    def __init__(self):
        super().__init__("simple_service_server")
        self.service_ = self.create_service(AddTwoInts, "add_two_ints", 
                                            self.serviceCallback)
        self.get_logger().info("Service add_two_ints Ready")

    def serviceCallback(self, request, response):
        response.sum = request.a + request.b
        self.get_logger().info(str(request.a) + " + " + 
                               str(request.b) + " = " + str(response.sum))  
        return response

def main(args=None):
    rclpy.init(args=args)
    simple_service_server = SimpleServiceServer()
    rclpy.spin(simple_service_server)
    simple_service_server.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()