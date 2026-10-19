#include "rclcpp/rclcpp.hpp"
#include "my_cpp_pkg/number_publisher_component.hpp"

using namespace std::chrono_literals;

namespace my_cpp_pkg {

NumberPublisherComponent::NumberPublisherComponent(const rclcpp::NodeOptions &options) : Node("number_publisher", options)
{
    number_ = 2;

    number_publisher_ = this->create_publisher<std_msgs::msg::Int64>("number", 10);
    number_timer_ = this->create_wall_timer(1000ms,
                                            std::bind(&NumberPublisherComponent::publishNumber, this));
    RCLCPP_INFO(this->get_logger(), "Number publisher has been started.");
}

void NumberPublisherComponent::publishNumber()
{
    auto msg = std_msgs::msg::Int64();
    msg.data = number_;
    number_publisher_->publish(msg);
}

} // namespace my_cpp_pkg

#include "rclcpp_components/register_node_macro.hpp"
RCLCPP_COMPONENTS_REGISTER_NODE(my_cpp_pkg::NumberPublisherComponent)