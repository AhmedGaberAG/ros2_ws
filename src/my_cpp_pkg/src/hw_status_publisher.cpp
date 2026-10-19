
#include "rclcpp/rclcpp.hpp"
#include "custom_interfaces/msg/hardware_status.hpp"

class HardwareStatusPublisher : public rclcpp::Node
{
public:
    HardwareStatusPublisher() : Node("hardware_status_publisher")
    {
        this->declare_parameter("publish_frequency", 1.0);
        publish_frequency_ = this->get_parameter("publish_frequency").as_double();

        pub_ = this->create_publisher<custom_interfaces::msg::HardwareStatus>(
            "hardware_status", 10);
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1) / publish_frequency_,
            std::bind(&HardwareStatusPublisher::publishHardwareStatus, this));
        RCLCPP_INFO(this->get_logger(), "Hardware status publisher has been started");
    }

private:
    void publishHardwareStatus()
    {
        auto msg = custom_interfaces::msg::HardwareStatus();
        msg.temperature = 57;
        msg.are_motor_ready = false;
        msg.debug_message = "Motors are too hot!";
        pub_->publish(msg);
    }

    rclcpp::Publisher<custom_interfaces::msg::HardwareStatus>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
    double publish_frequency_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<HardwareStatusPublisher>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}