
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_lifecycle/lifecycle_node.hpp"
#include "rclcpp_lifecycle/lifecycle_publisher.hpp"
#include "lifecycle_msgs/msg/state.hpp"
#include "std_msgs/msg/string.hpp"

#include <chrono>
#include <memory>
#include <thread>

using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

class SimpleLifecycleNode : public rclcpp_lifecycle::LifecycleNode
{
public:
  explicit SimpleLifecycleNode() : LifecycleNode("simple_lifecycle_node")
  {
    RCLCPP_INFO(get_logger(), "IN constructor");
  }

private:
  rclcpp::Subscription<std_msgs::msg::String>::SharedPtr sub_;

  // Configure: create ROS communications and prepare hardware
  CallbackReturn on_configure(const rclcpp_lifecycle::State & previous_state) override
  {
    (void)previous_state;
    sub_ = create_subscription<std_msgs::msg::String>(
      "chatter",
      10,
      std::bind(&SimpleLifecycleNode::msg_callback, this, std::placeholders::_1)
    );
    RCLCPP_INFO(get_logger(), "Lifecycle node on_configure() called.");
    return CallbackReturn::SUCCESS;
  }

  // Activate: enable hardware or begin operation
  CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override
  {
    RCLCPP_INFO(get_logger(), "IN on_activate");
    std::this_thread::sleep_for(std::chrono::seconds(2));
    return LifecycleNode::on_activate(previous_state);
  }

  // Deactivate: disable operation
  CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override
  {
    RCLCPP_INFO(get_logger(), "IN on_deactivate");
    return LifecycleNode::on_deactivate(previous_state);
  }

  // Cleanup: destroy resources created during configuration
  CallbackReturn on_cleanup(const rclcpp_lifecycle::State & previous_state) override
  {
    (void)previous_state;
    sub_.reset();
    RCLCPP_INFO(get_logger(), "Lifecycle node on_cleanup() called.");
    return CallbackReturn::SUCCESS;
  }

  // Shutdown: release resources
  CallbackReturn on_shutdown(const rclcpp_lifecycle::State & previous_state) override
  {
    (void)previous_state;
    sub_.reset();
    RCLCPP_INFO(get_logger(), "Lifecycle node on_shutdown() called.");
    return CallbackReturn::SUCCESS;
  }

  // Error handling
  CallbackReturn on_error(const rclcpp_lifecycle::State & previous_state) override
  {
    (void)previous_state;
    sub_.reset();
    RCLCPP_INFO(get_logger(), "Lifecycle node on_error() called.");
    // Return SUCCESS if recovery succeeds.
    return CallbackReturn::SUCCESS;
  }

  // Subscription callback
  void msg_callback(const std_msgs::msg::String::SharedPtr msg)
  {
    if (get_current_state().id() == lifecycle_msgs::msg::State::PRIMARY_STATE_ACTIVE)
    {
      RCLCPP_INFO(get_logger(), "I heard: %s", msg->data.c_str());
    }
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto simple_lifecycle_node = std::make_shared<SimpleLifecycleNode>();
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(simple_lifecycle_node->get_node_base_interface());
  try
  {
    executor.spin();
  }
  catch (const std::exception & e)
  {
    RCLCPP_ERROR(simple_lifecycle_node->get_logger(), "Executor exception: %s", e.what());
  }
  rclcpp::shutdown();
  return 0;
}
  