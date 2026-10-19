
#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/msg/string.hpp>

#include <functional>
#include <memory>

class SmartPhone : public rclcpp::Node
{
public:
    SmartPhone() : Node("smart_phone")
    {
        subscriber_ = this->create_subscription<example_interfaces::msg::String>(
                "robot_news",
                10,
                std::bind(
                    &SmartPhone::msg_callback,
                    this,
                    std::placeholders::_1
                )
            );    
        RCLCPP_INFO(this->get_logger(), "SmartPhone subscribed to /robot_news");
    }
private:
    void msg_callback(const example_interfaces::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Received news from robot: %s", msg->data.c_str());
    }
    rclcpp::Subscription<example_interfaces::msg::String>::SharedPtr subscriber_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto smart_phone = std::make_shared<SmartPhone>();
    rclcpp::spin(smart_phone);
    rclcpp::shutdown();
    return 0;
}
