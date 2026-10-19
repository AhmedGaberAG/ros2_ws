
#include <rclcpp/rclcpp.hpp>
#include <std_msgs/msg/int64.hpp>
#include <std_srvs/srv/set_bool.hpp>

#include <chrono>
#include <functional>
#include <memory>
#include <cinttypes>

using namespace std::placeholders;

class NumberCounter : public rclcpp::Node
{
public:
    NumberCounter() : Node("number_counter"), counter_(0)
    {
        subscriber_ = this->create_subscription<std_msgs::msg::Int64>(
            "number",
            10,
            std::bind(
                &NumberCounter::msg_callback,
                this,
                std::placeholders::_1
            )
        );

        publisher_ = this->create_publisher<std_msgs::msg::Int64>(
            "number_count",
            10
        );

        service_ = this->create_service<std_srvs::srv::SetBool>(
            "reset_number_count",
            std::bind(&NumberCounter::srv_callback, this, _1, _2)
        );

        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&NumberCounter::timer_callback, this)
        );

        RCLCPP_INFO(this->get_logger(), "Number Counter has been started.");
    }

private:
    void msg_callback(const std_msgs::msg::Int64::SharedPtr msg)
    {
        counter_ += msg->data;
        RCLCPP_INFO(this->get_logger(),
            "Received: %" PRId64 ", Current Count: %" PRId64,
            msg->data,
            counter_
        );
    }

    void srv_callback(
        const std_srvs::srv::SetBool::Request::SharedPtr request,
              std_srvs::srv::SetBool::Response::SharedPtr response)
    {
        if (request->data)
        {
            counter_ = 0;
            response->success = true;
            response->message = "Counter has been reset";
        }
        else
        {
            response->success = false;
            response->message = "Counter has not been reset"; 
        }
        
    }

    void timer_callback()
    {
        auto new_msg = std_msgs::msg::Int64();
        new_msg.data = counter_;
        publisher_->publish(new_msg);
    }
    
    rclcpp::Subscription<std_msgs::msg::Int64>::SharedPtr subscriber_;
    rclcpp::Publisher<std_msgs::msg::Int64>::SharedPtr publisher_;
    rclcpp::Service<std_srvs::srv::SetBool>::SharedPtr service_;
    rclcpp::TimerBase::SharedPtr timer_;
    int64_t counter_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto number_counter = std::make_shared<NumberCounter>();
    rclcpp::spin(number_counter);
    rclcpp::shutdown();
    return 0;
}
