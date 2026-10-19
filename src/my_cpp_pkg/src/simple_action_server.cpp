
#include "rclcpp/rclcpp.hpp"
#include "rclcpp_action/rclcpp_action.hpp"
#include "custom_interfaces/action/fibonacci.hpp"

#include <chrono>
#include <memory>
#include <thread>

using Fibonacci = custom_interfaces::action::Fibonacci;
using GoalHandleFibonacci = rclcpp_action::ServerGoalHandle<Fibonacci>;
using namespace std::chrono_literals;
using namespace std::placeholders;

class SimpleActionServer : public rclcpp::Node
{
public:
  SimpleActionServer() : Node("simple_action_server")
  {
    RCLCPP_INFO(this->get_logger(), "Starting the Server");
    action_server_ = rclcpp_action::create_server<Fibonacci>(
      this,
      "fibonacci",
      std::bind(&SimpleActionServer::handle_goal, this, _1, _2),
      std::bind(&SimpleActionServer::handle_cancel, this, _1),
      std::bind(&SimpleActionServer::handle_accepted, this, _1)
    );
  }

private:
  rclcpp_action::Server<Fibonacci>::SharedPtr action_server_;
  
  // Decide whether to accept the goal
  rclcpp_action::GoalResponse handle_goal(
    const rclcpp_action::GoalUUID & uuid,
    std::shared_ptr<const Fibonacci::Goal> goal)
  {
    (void)uuid;
    RCLCPP_INFO( this->get_logger(), "Received goal request with order %d", goal->order);
    return rclcpp_action::GoalResponse::ACCEPT_AND_EXECUTE;
  }

  // Handle cancellation requests
  rclcpp_action::CancelResponse handle_cancel(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    (void)goal_handle;
    RCLCPP_INFO(this->get_logger(), "Received cancel request");
    return rclcpp_action::CancelResponse::ACCEPT;
  }

  // Execute the accepted goal
  void handle_accepted(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    std::thread{std::bind(&SimpleActionServer::execute, this, goal_handle)}.detach();
  }

  void execute(const std::shared_ptr<GoalHandleFibonacci> goal_handle)
  {
    RCLCPP_INFO(this->get_logger(), "Executing Fibonacci goal");
    auto feedback = std::make_shared<Fibonacci::Feedback>();
    auto result = std::make_shared<Fibonacci::Result>();
    feedback->partial_sequence = {0, 1};
    int order = goal_handle->get_goal()->order;
    for (int i = 1; i < order; ++i)
    {
      if (goal_handle->is_canceling())
      {
        result->sequence = feedback->partial_sequence;
        goal_handle->canceled(result);
        RCLCPP_INFO(this->get_logger(), "Goal canceled");
        return;
      }
      feedback->partial_sequence.push_back(feedback->partial_sequence[i] + feedback->partial_sequence[i - 1]);
      RCLCPP_INFO(this->get_logger(), "Feedback: sequence size = %zu", feedback->partial_sequence.size());
      goal_handle->publish_feedback(feedback);
      std::this_thread::sleep_for(1s);
    }
    result->sequence = feedback->partial_sequence;
    goal_handle->succeed(result);
    RCLCPP_INFO(this->get_logger(), "Goal succeeded");
  }
};

int main(int argc, char ** argv)
{
  rclcpp::init(argc, argv);
  auto simple_action_server = std::make_shared<SimpleActionServer>();
  rclcpp::spin(simple_action_server);
  rclcpp::shutdown();
  return 0;
}
