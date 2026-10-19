
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "custom_interfaces/action/fibonacci.hpp"

#include <memory>

using Fibonacci = custom_interfaces::action::Fibonacci;
using GoalHandleFibonacci = rclcpp_action::ClientGoalHandle<Fibonacci>;
using namespace std::placeholders;

class SimpleActionClient : public rclcpp::Node
{
public:
  SimpleActionClient() : Node("simple_action_client")
  {
    action_client_ = rclcpp_action::create_client<Fibonacci>(this, "fibonacci");
    send_goal();
  }

private:
  rclcpp_action::Client<Fibonacci>::SharedPtr action_client_;
  void send_goal()
  {
    // Wait until the action server is available
    RCLCPP_INFO(this->get_logger(), "Waiting for action server...");
    action_client_->wait_for_action_server();
    
    // Create the goal
    auto goal_msg = Fibonacci::Goal();
    goal_msg.order = 10;
        
    // Configure callbacks
    auto send_goal_options = rclcpp_action::Client<Fibonacci>::SendGoalOptions();
    send_goal_options.goal_response_callback = std::bind(&SimpleActionClient::response_callback, this, _1);
    send_goal_options.feedback_callback =std::bind(&SimpleActionClient::feedback_callback, this, _1, _2);
    send_goal_options.result_callback = std::bind(&SimpleActionClient::result_callback, this, _1);

    // Send the goal asynchronously
    action_client_->async_send_goal(goal_msg, send_goal_options);
  }

  // Called when the server accepts or rejects the goal
  void response_callback(const GoalHandleFibonacci::SharedPtr & goal_handle)
  {
    if (!goal_handle)
    {
      RCLCPP_INFO(this->get_logger(), "Goal rejected :(");
    }
    else
    {
      RCLCPP_INFO(this->get_logger(), "Goal accepted :)");
    }
  }

  // Called whenever the server publishes feedback
  void feedback_callback(
    GoalHandleFibonacci::SharedPtr,
    const std::shared_ptr<const Fibonacci::Feedback> feedback)
  {
    RCLCPP_INFO(this->get_logger(), "Received feedback: sequence size = %zu", feedback->partial_sequence.size());
  }

  // Called when the action finishes
  void result_callback( const GoalHandleFibonacci::WrappedResult & result)
  {
    switch (result.code)
    {
      case rclcpp_action::ResultCode::SUCCEEDED:
        RCLCPP_INFO(this->get_logger(), "Result received successfully:");
        for (const auto number : result.result->sequence)
        {
          RCLCPP_INFO(this->get_logger(), "%d", number);
        }
        break;
      case rclcpp_action::ResultCode::ABORTED:
        RCLCPP_ERROR(this->get_logger(), "Goal was aborted");
        break;
      case rclcpp_action::ResultCode::CANCELED:
        RCLCPP_WARN(this->get_logger(), "Goal was canceled");
        break;
      default:
        RCLCPP_ERROR(this->get_logger(), "Unknown result code");
        break;
    }
    rclcpp::shutdown();
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto simple_action_client = std::make_shared<SimpleActionClient>();
  rclcpp::spin(simple_action_client);
  if (rclcpp::ok())
  {
    rclcpp::shutdown();
  }
  return 0;
}
