
#include "rclcpp/rclcpp.hpp"
#include "custom_interfaces/msg/hardware_status.hpp"

#include <memory>

class HardwareStatusSubscriber : public rclcpp::Node
{
public:
    HardwareStatusSubscriber() : Node("hardware_status_subscriber")
    {
        sub_ = this->create_subscription<custom_interfaces::msg::HardwareStatus>(
            "hardware_status", 10,
            std::bind(&HardwareStatusSubscriber::statusCallback, this, std::placeholders::_1));
        RCLCPP_INFO(this->get_logger(), "Hardware status subscriber has been started");
    }
private:
    void statusCallback(const custom_interfaces::msg::HardwareStatus::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Received hardware status: Temperature: %ld, Motors Ready: %s, Debug Message: %s",
                    msg->temperature,
                    msg->are_motor_ready ? "true" : "false",
                    msg->debug_message.c_str());
    }

    rclcpp::Subscription<custom_interfaces::msg::HardwareStatus>::SharedPtr sub_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto hardware_status_subscriber = std::make_shared<HardwareStatusSubscriber>();
    rclcpp::spin(hardware_status_subscriber);
    rclcpp::shutdown();
    return 0;     
}