#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node
from example_interfaces.srv import AddTwoInts
import sys

def main(args=None):
    rclpy.init(args=args)
    if len(sys.argv) != 3:
        print("wrong number of arguments! Usage: simpel_service_client A B")
        return -1
    
    node = Node("simple_service_client")
    client = node.create_client(AddTwoInts, 'add_two_ints')
    while not client.wait_for_service(1.0):
        node.get_logger().warn("Service not available, waiting again...")

    request = AddTwoInts.Request()
    request.a = int(sys.argv[1])
    request.b = int(sys.argv[2])

    future = client.call_async(request)
    rclpy.spin_until_future_complete(node, future)

    try:
        response = future.result()
        node.get_logger().info(str(request.a) + " + " + 
                               str(request.b) + " = " + str(response.sum))  

    except Exception as e:
        node.get_logger().error("Service call failed %r" %(e,))

    node.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()