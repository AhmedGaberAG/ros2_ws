#!/usr/bin/env python3 

import rclpy
from rclpy.node import Node
from custom_interfaces.srv import SetLed
from functools import partial

class Battery(Node):
    def __init__(self):
        super().__init__("battery")
        self.battery_state_ = "full"
        self.last_time_battery_state_changed_ = self.get_current_time_seconds()
        self.battery_timer_ = self.create_timer(0.1, self.check_battery_state)
        self.get_logger().info("Battery node has been started")

    def get_current_time_seconds(self):
        secs, nsecs = self.get_clock().now().seconds_nanoseconds()
        return secs + nsecs / 1000000000.0

    def check_battery_state(self):
        time_now = self.get_current_time_seconds()
        if self.battery_state_ == "full":
            if time_now - self.last_time_battery_state_changed_ > 4.0:
                self.battery_state_ = "empty"
                self.get_logger().info("Battery is empty! Charging battery...")
                self.last_time_battery_state_changed_ = time_now
                self.call_set_led_server(3, 1)
        else:
            if time_now - self.last_time_battery_state_changed_ > 6.0:
                self.battery_state_ = "full"
                self.get_logger().info("Battery is now full again.")
                self.last_time_battery_state_changed_ = time_now
                self.call_set_led_server(3, 0)

    def call_set_led_server(self, led_number, state):
        self.client_ = self.create_client(SetLed, "set_led")

        while not self.client_.wait_for_service(1.0):
            self.get_logger().warn(
                "Service not available, waiting again..."
            )

        self.request_ = SetLed.Request()
        self.request_.led_number = led_number
        self.request_.state = state

        self.future_ = self.client_.call_async(self.request_)
        self.future_.add_done_callback(
            partial(
                self.responseCallback,
                led_number=led_number,
                state=state
            )
        )


    def responseCallback(self, future, led_number, state):
        try:
            response = future.result()
            self.get_logger().info(str(response.success))
        except Exception as e:
            self.get_logger().error("Service call failed %r" % (e,))

def main(args=None):

    rclpy.init(args=args)
    battery = Battery()
    rclpy.spin(battery)
    battery.destroy_node()
    rclpy.shutdown()

if __name__ == "__main__":
    main()