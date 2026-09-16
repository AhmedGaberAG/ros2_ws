#include <rclcpp/rclcpp.hpp>
#include <chrono>


class MyNode : public rclcpp::Node
{
public:
    MyNode() : Node("my_node"), counter_(0)
    {
        RCLCPP_INFO(this->get_logger(), "Hello, ROS 2!");
        
        timer_ = this->create_wall_timer(
            std::chrono::seconds(1),
            std::bind(&MyNode::timer_callback, this)
        );
    }
private:
    void timer_callback()
    {
        counter_++;
        RCLCPP_INFO(
            this->get_logger(),
            "Timer callback triggered! Count: %d",
            counter_
        );
    }

    rclcpp::TimerBase::SharedPtr timer_;
    int counter_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto node = std::make_shared<MyNode>();
    rclcpp::spin(node);
   
    // Destroy node
    node.reset();
    rclcpp::shutdown();

    return 0;
}