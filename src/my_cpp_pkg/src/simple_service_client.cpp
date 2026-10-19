
#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/add_two_ints.hpp>

#include <chrono>
#include<memory>
#include <functional>

using namespace std::chrono_literals;
using std::placeholders::_1;

class SimpleServiceClient : public rclcpp::Node
{
public:
    SimpleServiceClient(int a, int b) : Node("simple_service_client"), a_(a), b_(b)
    {
        client_ = this->create_client<example_interfaces::srv::AddTwoInts>("add_two_ints");
        
        auto request = std::make_shared<example_interfaces::srv::AddTwoInts::Request>();
        request->a = a_;
        request->b = b_;

        while (!client_->wait_for_service(1s)) 
        {
            if (!rclcpp::ok()) 
            {
                RCLCPP_ERROR(this->get_logger(), "Interrupted while waiting for the service. Exiting.");
                return;
            }
            RCLCPP_INFO(this->get_logger(), "service not available, waiting again...");
        }

        client_->async_send_request(request,
            std::bind(&SimpleServiceClient::response_callback, this, _1)
        );
    }
private:
    void response_callback(rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedFuture future)
    {
        auto response = future.get();
        if (!response) 
        {
            RCLCPP_ERROR(this->get_logger(), "Service call failed");
            return;
        }
        RCLCPP_INFO(this->get_logger(), "%d + %d = %ld", a_, b_, response->sum);
    }

    rclcpp::Client<example_interfaces::srv::AddTwoInts>::SharedPtr client_;
    int a_;
    int b_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    if (argc != 3) {
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Wrong number of arguments! Usage: simple_service_client A B");
    return 1;
    }
    auto simple_service_client = std::make_shared<SimpleServiceClient>(atoi(argv[1]), atoi(argv[2]));
    rclcpp::spin(simple_service_client);
    rclcpp::shutdown();
    return 0;
}