#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64
from std_srvs.srv import SetBool

class NumberCounter(Node):
    def __init__(self):
        super().__init__("number_counter")
        self.declare_parameter("counter", 0)        
        self.counter_ = self.get_parameter("counter").value

        self.publisher_ = self.create_publisher(Int64, "number_count", 10)
        self.subscriber_ = self.create_subscription(
            Int64,
            "number",
            self.msgCallback,
            10
        )
        self.service_ = self.create_service(
            SetBool, 
            "reset_number_count", 
            self.serviceCallback
        )
        self.get_logger().info("Number Counter Has Been Started.")

    def msgCallback(self, msg):
        self.counter_ += msg.data
        new_msg = Int64()
        new_msg.data = self.counter_
        self.publisher_.publish(new_msg)
        self.get_logger().info("Received: %d, Current Count: %d"
                                % (msg.data, self.counter_))

    def serviceCallback(self, request, response):
        if request.data:
            self.counter_ = 0
            response.success = True
            response.message = "Counter has been reset"
        else:
            response.success = False
            response.message = "Counter has not been reset"
        return response

        
def main(args=None):
    rclpy.init(args=args)
    number_counter = NumberCounter()
    rclpy.spin(number_counter)
    number_counter.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()

