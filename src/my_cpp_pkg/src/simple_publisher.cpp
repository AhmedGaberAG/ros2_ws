
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/string.hpp>

#include <chrono>
#include <functional>
#include <memory>
#include <string>

class SimplePublisher : public rclcpp::Node
{
public:
    SimplePublisher() : Node("simple_publisher"), counter_(0)
    {
        this->declare_parameter("publish_frequency", 1.0);
        publish_frequency_ = this->get_parameter("publish_frequency").as_double();

        publisher_ = this->create_publisher<std_msgs::msg::String>(
            "chatter", 10
        );

        timer_ = this->create_wall_timer(
            std::chrono::seconds((int) (1.0 / publish_frequency_)),
            std::bind(&SimplePublisher::timer_callback, this)
        );

        RCLCPP_INFO(this->get_logger(), "Publishing messages at a frequency of %f Hz", publish_frequency_);
    }
private:
    void timer_callback()
    {
        auto msg = std_msgs::msg::String();
        msg.data = "Hello, ROS 2! " + std::to_string(counter_);
        publisher_->publish(msg);
        RCLCPP_INFO(this->get_logger(), "Publishing: '%s'", msg.data.c_str());
        counter_++;
    }
    rclcpp::Publisher<std_msgs::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    int counter_;
    double publish_frequency_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto simple_publisher = std::make_shared<SimplePublisher>();
    rclcpp::spin(simple_publisher);
    rclcpp::shutdown();
    return 0;
}
