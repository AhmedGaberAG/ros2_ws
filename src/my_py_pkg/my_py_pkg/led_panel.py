#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from custom_interfaces.msg import LedStateArray
from custom_interfaces.srv import SetLed

class LedPanel(Node):
    def __init__(self):
        super().__init__("led_panel")
        self.declare_parameter("led_state", [0, 0, 0])
        self.declare_parameter("frequency", 0.25)       
        self.led_state_ = self.get_parameter("led_state").value
        self.frequency_ = self.get_parameter("frequency").value
        
        self.publisher_ = self.create_publisher(LedStateArray, "led_panel_state", 10)
        self.service_ = self.create_service(SetLed, "set_led", self.serviceCallback)
        self.timer_ = self.create_timer(1.0 / self.frequency_, self.timerCallback)
        self.get_logger().info("Led panel node has been started.")

    def timerCallback(self):
        msg = LedStateArray()
        msg.led_states = self.led_state_
        self.publisher_.publish(msg)

    def serviceCallback(self, request, response):
        led_number = request.led_number
        state = request.state

        if led_number > len(self.led_state_) or led_number <= 0:
            response.success = False
            return response 

        if state not in [0, 1]:
            response.success = False
            return response           

        self.led_state_[led_number - 1] = state
        response.success = True
        self.timerCallback()
        return response    

def main(args=None):
    rclpy.init(args=args)
    led_panel = LedPanel()
    rclpy.spin(led_panel)
    led_panel.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()