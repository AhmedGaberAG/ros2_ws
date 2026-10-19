
#include "rclcpp/rclcpp.hpp"
#include "custom_interfaces/msg/led_state_array.hpp"
#include "custom_interfaces/srv/set_led.hpp"

class LedPanelNode : public rclcpp::Node
{
public:
    LedPanelNode() : Node("led_panel"), led_states_(3, 0)
    {
        led_states_publisher_ =
            this->create_publisher<custom_interfaces::msg::LedStateArray>("led_states", 10);
        led_states_timer_ =
            this->create_wall_timer(std::chrono::seconds(4),
                                    std::bind(&LedPanelNode::publishLedStates, this));
        set_led_service_ = this->create_service<custom_interfaces::srv::SetLed>(
            "set_led",
            std::bind(&LedPanelNode::callbackSetLed, this, std::placeholders::_1, std::placeholders::_2));
        RCLCPP_INFO(this->get_logger(), "Led panel node has been started");
    }

private:
    void publishLedStates()
    {
        auto msg = custom_interfaces::msg::LedStateArray();
        msg.led_states = led_states_;
        led_states_publisher_->publish(msg);
    }

    void callbackSetLed(const custom_interfaces::srv::SetLed::Request::SharedPtr request,
                        const custom_interfaces::srv::SetLed::Response::SharedPtr response)
    {
        int64_t led_number = request->led_number;
        int64_t state = request->state;

        if (led_number > (int64_t)led_states_.size() || led_number <= 0)
        {
            response->success = false;
            return;
        }

        if (state != 0 && state != 1)
        {
            response->success = false;
            return;
        }

        led_states_.at(led_number - 1) = state;
        response->success = true;
        publishLedStates();
    }

    std::vector<int64_t> led_states_;

    rclcpp::Publisher<custom_interfaces::msg::LedStateArray>::SharedPtr led_states_publisher_;
    rclcpp::TimerBase::SharedPtr led_states_timer_;
    rclcpp::Service<custom_interfaces::srv::SetLed>::SharedPtr set_led_service_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<LedPanelNode>();
    rclcpp::spin(node);
    rclcpp::shutdown();
    return 0;
}
