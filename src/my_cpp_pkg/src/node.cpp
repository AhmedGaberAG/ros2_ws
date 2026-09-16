#include <rclcpp/rclcpp.hpp>
#include <chrono>

int counter = 0;

void timer_callback()
{
    counter++;

    RCLCPP_INFO(
        rclcpp::get_logger("my_node"),
        "Timer callback triggered! Count: %d",
        counter
    );
}

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<rclcpp::Node>("my_node");
    RCLCPP_INFO(node->get_logger(), "Hello, ROS 2!");
    auto timer = node->create_wall_timer(
        std::chrono::seconds(1),
        timer_callback
    );
    rclcpp::spin(node);
   
    // Destroy timer
    timer->cancel();
    timer.reset();
   
    // Destroy node
    node.reset();
    rclcpp::shutdown();

    return 0;
}