
#include <rclcpp/rclcpp.hpp>
#include <example_interfaces/srv/add_two_ints.hpp>

#include <cinttypes>
#include <functional>
#include <memory>

// using std::placeholders::_1, std::placeholders::_2;
using namespace std::placeholders;

class SimpleServiceServer : public rclcpp::Node
{
public:
    SimpleServiceServer() : Node("simple_service_server")
    {
        server_ = this->create_service<example_interfaces::srv::AddTwoInts>(
            "add_two_ints",
            std::bind(
                &SimpleServiceServer::callbackAddTwoInts,
                this, _1, _2
            )
        );
        RCLCPP_INFO(this->get_logger(), "Service /add_two_ints is ready.");
    }

private:
    void callbackAddTwoInts(
        const example_interfaces::srv::AddTwoInts::Request::SharedPtr request,
        example_interfaces::srv::AddTwoInts::Response::SharedPtr response)
    {
        response->sum = request->a + request->b;

        RCLCPP_INFO(this->get_logger(),
            "%" PRId64 " + %" PRId64 " = %" PRId64,
            request->a,
            request->b,
            response->sum
        );
    }
    rclcpp::Service<example_interfaces::srv::AddTwoInts>::SharedPtr server_;
};

int main(int argc, char **argv)
{
    rclcpp::init(argc, argv);
    auto simple_service_server =std::make_shared<SimpleServiceServer>();
    rclcpp::spin(simple_service_server);
    rclcpp::shutdown();
    return 0;
}
