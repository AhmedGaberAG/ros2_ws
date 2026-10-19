
#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/msg/string.hpp>

#include <chrono>
#include <functional>
#include <memory>
#include <string>

class RobotNewsStation : public rclcpp::Node
{
public:
    RobotNewsStation() : Node("robot_news_station")
    {
        this->declare_parameter("robot_name", "R2D2");
        robot_name_ = this->get_parameter("robot_name").as_string();

        publisher_ =this->create_publisher<example_interfaces::msg::String>(
            "robot_news", 10
        );
        timer_ = this->create_wall_timer(
            std::chrono::milliseconds(500),
            std::bind(&RobotNewsStation::timer_callback, this)
        );
        RCLCPP_INFO(this->get_logger(), "Robot News Station initialized with frequency: 2 Hz");
    }
private:
    void timer_callback()
    {
        auto msg = example_interfaces::msg::String();
        msg.data =
            "Hi, this is '" + robot_name_ +
            "' from the Robot News Station.";
        publisher_->publish(msg);
    }

    rclcpp::Publisher<example_interfaces::msg::String>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;
    std::string robot_name_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto robot_news_station = std::make_shared<RobotNewsStation>();
    rclcpp::spin(robot_news_station);
    rclcpp::shutdown();
    return 0;
}
