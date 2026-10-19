
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

#include <chrono>
#include <memory>
#include <thread>

using namespace std::chrono_literals;

class SimpleSingleThreadedExecutor : public rclcpp::Node
{
public:
    SimpleSingleThreadedExecutor() : Node("simple_single_threaded_executor")
    {
        // 1. Timer: Read LiDAR every 0.5 seconds
        lidar_timer_ = create_wall_timer( 
            500ms,
            std::bind(&SimpleSingleThreadedExecutor::lidar_callback, this)
        );

        // 2. Timer: Control motors every 1 second
        motor_timer_ = create_wall_timer(
            1s,
            std::bind(&SimpleSingleThreadedExecutor::motor_callback,this)
        );

        // 3. Subscriber: Emergency stop
        stop_subscriber_ = create_subscription<std_msgs::msg::String>(
            "/emergency_stop",
            10,
            std::bind(&SimpleSingleThreadedExecutor::stop_callback, this, std::placeholders::_1)
        );
    }

private:
    void lidar_callback()
    {
        RCLCPP_INFO(get_logger(), "LiDAR callback: reading sensor...");
        // Simulate a slow LiDAR operation
        std::this_thread::sleep_for(2s);
        RCLCPP_INFO(get_logger(), "LiDAR callback: DONE");
    }

    void motor_callback()
    {
        RCLCPP_INFO(get_logger(), "Motor callback: controlling motors");
    }

    void stop_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_WARN(get_logger(), "EMERGENCY STOP: %s", msg->data.c_str());
    }

    rclcpp::TimerBase::SharedPtr lidar_timer_;
    rclcpp::TimerBase::SharedPtr motor_timer_;
    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr stop_subscriber_;
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto simple_single_threaded_executor = std::make_shared<SimpleSingleThreadedExecutor>();
    rclcpp::executors::SingleThreadedExecutor executor;
    executor.add_node(simple_single_threaded_executor);
    executor.spin();
    executor.remove_node(simple_single_threaded_executor);
    rclcpp::shutdown();
    return 0;
}
