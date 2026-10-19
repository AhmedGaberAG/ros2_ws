
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "rclcpp_lifecycle/lifecycle_publisher.hpp"
#include "std_msgs/msg/int64.hpp"

#include <chrono>
#include <memory>

using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;
using namespace std::chrono_literals;

class NumberPublisherLifecycleNode : public rclcpp_lifecycle::LifecycleNode
{
public:
    NumberPublisherLifecycleNode() : LifecycleNode("number_publisher_life_cycle_node")
    {
        RCLCPP_INFO(get_logger(), "IN constructor");
        declare_parameter<int64_t>("number", 1);
        declare_parameter<double>("frequency", 1.0);

        number_ = get_parameter("number").as_int();
        frequency_ = get_parameter("frequency").as_double();        
    }

private:
    int64_t number_{1};
    double frequency_{1.0};

    rclcpp_lifecycle::LifecyclePublisher<std_msgs::msg::Int64>::SharedPtr publisher_;
    rclcpp::TimerBase::SharedPtr timer_;

    // Configure: create publisher and timer
    CallbackReturn on_configure(const rclcpp_lifecycle::State & previous_state) override
    {
        (void)previous_state;
        RCLCPP_INFO(get_logger(), "IN on_configure");
        publisher_ = create_publisher<std_msgs::msg::Int64>("number", 10);
        auto period = std::chrono::duration_cast<std::chrono::nanoseconds>(std::chrono::duration<double>(1.0 / frequency_));
        timer_ = create_wall_timer(period, std::bind(&NumberPublisherLifecycleNode::timer_callback, this));
        // Do not publish until activation
        timer_->cancel();
        return CallbackReturn::SUCCESS;
    }

    // Activate: enable publishing
    CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override
    {
        RCLCPP_INFO(get_logger(), "IN on_activate");
        auto result = LifecycleNode::on_activate(previous_state);
        if (result != CallbackReturn::SUCCESS) return result;
        timer_->reset();
        return CallbackReturn::SUCCESS;
    }

    // Deactivate: stop publishing
    CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override
    {
        RCLCPP_INFO(get_logger(), "IN on_deactivate");
        timer_->cancel();
        return LifecycleNode::on_deactivate(previous_state);
    }

    // Cleanup: destroy resources
    CallbackReturn on_cleanup(const rclcpp_lifecycle::State & previous_state) override
    {
        (void)previous_state;
        RCLCPP_INFO(get_logger(), "IN on_cleanup");
        timer_.reset();
        publisher_.reset();
        return CallbackReturn::SUCCESS;
    }

    // Shutdown: release resources
    CallbackReturn on_shutdown(const rclcpp_lifecycle::State & previous_state) override
    {
        (void)previous_state;
        RCLCPP_INFO(get_logger(), "IN on_shutdown");
        if (timer_)
        {
            timer_->cancel();
            timer_.reset();
        }

        publisher_.reset();
        return CallbackReturn::SUCCESS;
    }

    // Error handling
    CallbackReturn on_error(const rclcpp_lifecycle::State & previous_state) override
    {
        (void)previous_state;
        RCLCPP_INFO(get_logger(), "IN on_error");
        if (timer_)
        {
            timer_->cancel();
            timer_.reset();
        }
        publisher_.reset();
        return CallbackReturn::SUCCESS;
    }

    // Timer callback
    void timer_callback()
    {
        if (!publisher_ || !publisher_->is_activated()) return;
        auto msg = std_msgs::msg::Int64();
        msg.data = number_;
        publisher_->publish(msg);
        RCLCPP_INFO(get_logger(), "Publishing: %ld", static_cast<long>(number_));
        number_++;
    }
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    auto number_publisher_lifecycle_node =std::make_shared<NumberPublisherLifecycleNode>();
    rclcpp::spin(number_publisher_lifecycle_node->get_node_base_interface());
    rclcpp::shutdown();
    return 0;
}
