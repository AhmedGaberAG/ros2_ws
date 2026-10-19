
#include "rclcpp/rclcpp.hpp"
#include "std_msgs/msg/string.hpp"

#include <chrono>
#include <memory>
#include <thread>
#include <functional>

using namespace std::chrono_literals;

class SimpleMultiThreadedExecutor : public rclcpp::Node
{
public:
    SimpleMultiThreadedExecutor() : Node("simple_multi_threaded_executor")
    {
        // Callback groups
        lidar_group_ = create_callback_group(rclcpp::CallbackGroupType::Reentrant);
        motor_stop_group_ = create_callback_group(rclcpp::CallbackGroupType::MutuallyExclusive);

        // 1. Timer: Read LiDAR every 0.5 seconds
        lidar_timer_ = create_wall_timer(
            500ms,
            std::bind(&SimpleMultiThreadedExecutor::lidar_callback, this),
            lidar_group_
        );

        // 2. Timer: Control motors every 1 second
        motor_timer_ = create_wall_timer(
            1s,
            std::bind(&SimpleMultiThreadedExecutor::motor_callback, this),
            motor_stop_group_
        );

        // 3. Subscriber: Emergency stop
        rclcpp::SubscriptionOptions options;
        options.callback_group = motor_stop_group_;

        stop_subscriber_ = create_subscription<std_msgs::msg::String>(
            "/emergency_stop",
            10,
            std::bind(&SimpleMultiThreadedExecutor::stop_callback, this, std::placeholders::_1),
            options
        );
    }

private:
    void lidar_callback()
    {
        RCLCPP_INFO(get_logger(), "LiDAR START | Thread: %zu", std::hash<std::thread::id>{}(std::this_thread::get_id()));
        std::this_thread::sleep_for(2s);
        RCLCPP_INFO(get_logger(), "LiDAR DONE | Thread: %zu", std::hash<std::thread::id>{}(std::this_thread::get_id()));
    }

    void motor_callback()
    {
        RCLCPP_INFO(get_logger(), "Motor START | Thread: %zu", std::hash<std::thread::id>{}(std::this_thread::get_id()));
        std::this_thread::sleep_for(2s);
        RCLCPP_INFO(get_logger(), "Motor DONE | Thread: %zu", std::hash<std::thread::id>{}(std::this_thread::get_id()));
    }

    void stop_callback(const std_msgs::msg::String::SharedPtr msg)
    {
        RCLCPP_WARN(get_logger(), "EMERGENCY STOP: %s | Thread: %zu", msg->data.c_str(), std::hash<std::thread::id>{}(std::this_thread::get_id()));
    }

    rclcpp::CallbackGroup::SharedPtr lidar_group_;
    rclcpp::CallbackGroup::SharedPtr motor_stop_group_;

    rclcpp::TimerBase::SharedPtr lidar_timer_;
    rclcpp::TimerBase::SharedPtr motor_timer_;

    rclcpp::Subscription<std_msgs::msg::String>::SharedPtr stop_subscriber_;
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto simple_multi_threaded_executor = std::make_shared<SimpleMultiThreadedExecutor>();
    rclcpp::executors::MultiThreadedExecutor executor(rclcpp::ExecutorOptions(), 3);
    executor.add_node(simple_multi_threaded_executor);
    executor.spin();
    executor.remove_node(simple_multi_threaded_executor);
    rclcpp::shutdown();
    return 0;
}
