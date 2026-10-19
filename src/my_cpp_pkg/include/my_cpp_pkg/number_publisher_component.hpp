#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/int64.hpp"

namespace my_cpp_pkg {

class NumberPublisherComponent : public rclcpp::Node
{
public:
    NumberPublisherComponent(const rclcpp::NodeOptions &options);

private:
    void publishNumber();

    int number_;
    rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr number_publisher_;
    rclcpp::TimerBase::SharedPtr number_timer_;
};

} // namespace my_cpp_pkg
