
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/int64.hpp>

#include <chrono>
#include <functional>
#include <memory>

class NumberPublisher : public rclcpp::Node
{
public:
    NumberPublisher() : Node("number_publisher")
    {
        this->declare_parameter("number", 2);
        number_ = this->get_parameter("number").as_int();

        publisher_ = this->create_publisher<std_msgs::msg::Int64>(
            "number", 10
        );
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&NumberPublisher::timer_callback, this)
        );
        RCLCPP_INFO(this->get_logger(), "Publishing messages at a frequency of 1 Hz");
    }
private:
    void timer_callback()
    {
        auto msg = std_msgs::msg::Int64();
        msg.data = number_;
        publisher_->publish(msg);
    }
    rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    int number_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto number_publisher = std::make_shared<NumberPublisher>();
    rclcpp::spin(number_publisher);
    rclcpp::shutdown();
    return 0;
}
