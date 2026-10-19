
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

#include <functional>
#include <memory>

class SimpleSubscriber : public rclcpp::Node
{
public:
    SimpleSubscriber() : Node("simple_subscriber")
    {
        subscriber_ = this->create_subscription<std_msgs::msg::String>(
            "chatter",
            10,
            std::bind(
                &SimpleSubscriber::msg_callback,
                this,
                std::placeholders::_1
            )
        );
        RCLCPP_INFO(this->get_logger(), "Subscribed to topic '/chatter'");
    }
private:
    void msg_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_INFO(this->get_logger(), "Received: '%s'", msg->data.c_str());
    }
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr subscriber_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto simple_subscriber = std::make_shared<SimpleSubscriber>();
    rclcpp::spin(simple_subscriber);
    rclcpp::shutdown();
    return 0;
}
