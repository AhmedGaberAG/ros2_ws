#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String

class RobotNewsStation(Node):
    def __init__(self):
        super().__init__("robot_news_station")
        self.declare_parameter("robot_name", "C390")
        self.declare_parameter("frequency", 2.0)     
        self.robot_name_ = self.get_parameter("counter").value
        self.frequency_ = self.get_parameter("frequency").value

        self.publisher_ = self.create_publisher(String, "robot_news", 10)
        self.timer = self.create_timer(1.0 / self.frequency_, self.publishNews) 
        self.get_logger().info("Robot News Station initialized with frequency: %f Hz"
                                % self.frequency_)

    def publishNews(self):
        msg = String() 
        msg.data =  "Hi, this is " + str(self.robot_name_) + \
            " from the Robot News Station."
        self.publisher_.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    robot_news_station = RobotNewsStation()
    rclpy.spin(robot_news_station)
    robot_news_station.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()