#!/usr/bin/env python3
import rclpy
from rclpy.executors import SingleThreadedExecutor
from my_py_pkg.node1 import Node1
from my_py_pkg.node2 import Node2

def main(args=None):
    rclpy.init(args=args)
    # Load components into the same process
    node1 = Node1()
    node2 = Node2()
    # Container executor
    executor = SingleThreadedExecutor()
    executor.add_node(node1)
    executor.add_node(node2)
    executor.spin()
    node1.destroy_node()
    node2.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()
