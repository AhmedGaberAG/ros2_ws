
#include <rclcpp/rclcpp.hpp>
#include <std_srvs/srv/set_bool.hpp>

#include <chrono>
#include <memory>
#include <functional>
#include <string>

using namespace std::chrono_literals;
using std::placeholders::_1;

class NumberClient : public rclcpp::Node
{
public:
    NumberClient(bool data) : Node("number_client"), data_(data)
{
    client_ = this->create_client<std_srvs::srv::SetBool>("reset_number_count");

    auto request = std::make_shared<std_srvs::srv::SetBool::Request>();
    request->data = data_;

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
        std::bind(&NumberClient::response_callback, this, _1)
    );
}
private:
    void response_callback(rclcpp::Client<std_srvs::srv::SetBool>::SharedFuture future)
    {
        auto response = future.get();
        if (!response) 
        {
            RCLCPP_ERROR(this->get_logger(), "Service call failed");
            return;
        }
        RCLCPP_INFO(this->get_logger(), "Success: %s", response->success ? "true" : "false");
        RCLCPP_INFO(this->get_logger(), "Message: %s", response->message.c_str());
    }
    rclcpp::Client<std_srvs::srv::SetBool>::SharedPtr client_;
    bool data_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    if(argc != 2){
    RCLCPP_ERROR(rclcpp::get_logger("rclcpp"), "Wrong number of arguments!\n"
            "Usage: number_client [True or False]");
    return 1;
    }
    auto data = std::string(argv[1]) == "True" || std::string(argv[1]) == "true" ? true : false;
    auto number_client = std::make_shared<NumberClient>(data);
    rclcpp::spin(number_client);
    rclcpp::shutdown(); 
    return 0;
}