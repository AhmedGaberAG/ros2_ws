cmake_minimum_required(VERSION 3.8)
project(my_cpp_pkg)

# Add compile options for GCC and Clang
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# Find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(std_srvs REQUIRED)
find_package(example_interfaces REQUIRED)
find_package(custom_interfaces REQUIRED)
find_package(rcl_interfaces REQUIRED)
find_package(rclcpp_action REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(lifecycle_msgs REQUIRED)
find_package(rclcpp_components REQUIRED)

# Add include directories
include_directories(include)

# Basic node
add_executable(my_node src/node.cpp)
ament_target_dependencies(my_node rclcpp)

# Publisher and subscriber
add_executable(simple_publisher src/simple_publisher.cpp)
ament_target_dependencies(simple_publisher rclcpp std_msgs)

add_executable(simple_subscriber src/simple_subscriber.cpp)
ament_target_dependencies(simple_subscriber rclcpp std_msgs)

# Robot news publisher and subscriber
add_executable(robot_news_station src/robot_news_station.cpp)
ament_target_dependencies(robot_news_station rclcpp example_interfaces)

add_executable(smart_phone src/smart_phone.cpp)
ament_target_dependencies(smart_phone rclcpp example_interfaces)

# Number publisher, counter, client and lifecycle node
add_executable(number_publisher src/number_publisher.cpp)
ament_target_dependencies(number_publisher rclcpp std_msgs)

add_executable(number_counter src/number_counter.cpp)
ament_target_dependencies(number_counter rclcpp std_msgs std_srvs)

add_executable(number_client src/number_client.cpp)
ament_target_dependencies(number_client rclcpp std_srvs)

add_executable(number_publisher_lifecycle_node src/number_publisher_lifecycle_node.cpp)
ament_target_dependencies(number_publisher_lifecycle_node rclcpp rclcpp_lifecycle std_msgs)

# Service server and client
add_executable(simple_service_server src/simple_service_server.cpp)
ament_target_dependencies(simple_service_server rclcpp example_interfaces)

add_executable(simple_service_client src/simple_service_client.cpp)
ament_target_dependencies(simple_service_client rclcpp example_interfaces)

# Hardware status publisher and subscriber
add_executable(hw_status_publisher src/hw_status_publisher.cpp)
ament_target_dependencies(hw_status_publisher rclcpp custom_interfaces)

add_executable(hw_status_subscriber src/hw_status_subscriber.cpp)
ament_target_dependencies(hw_status_subscriber rclcpp custom_interfaces)

# LED panel and battery nodes
add_executable(led_panel src/led_panel.cpp)
ament_target_dependencies(led_panel rclcpp custom_interfaces)

add_executable(battery src/battery.cpp)
ament_target_dependencies(battery rclcpp custom_interfaces)

# Simple parameter node
add_executable(simple_parameter src/simple_parameter.cpp)
ament_target_dependencies(simple_parameter rclcpp rcl_interfaces)

# Simple action server and client
add_executable(simple_action_server src/simple_action_server.cpp)
ament_target_dependencies(simple_action_server rclcpp rclcpp_action custom_interfaces)

add_executable(simple_action_client src/simple_action_client.cpp)
ament_target_dependencies(simple_action_client rclcpp rclcpp_action custom_interfaces)

# Count until action server and client
add_executable(count_until_server src/count_until_server.cpp)
ament_target_dependencies(count_until_server rclcpp rclcpp_action custom_interfaces)

add_executable(count_until_client src/count_until_client.cpp)
ament_target_dependencies(count_until_client rclcpp rclcpp_action custom_interfaces)

add_executable(count_until_server_queue_goals src/count_until_server_queue_goals.cpp)
ament_target_dependencies(count_until_server_queue_goals rclcpp rclcpp_action custom_interfaces)

# Move robot action server and client
add_executable(move_robot_server src/move_robot_server.cpp)
ament_target_dependencies(move_robot_server rclcpp rclcpp_action custom_interfaces)

add_executable(move_robot_client src/move_robot_client.cpp)
ament_target_dependencies(move_robot_client rclcpp rclcpp_action custom_interfaces example_interfaces)

# Simple lifecycle node
add_executable(simple_lifecycle_node src/simple_lifecycle_node.cpp)
ament_target_dependencies(simple_lifecycle_node rclcpp rclcpp_lifecycle std_msgs)

# Simple single-threaded executor
add_executable(simple_single_threaded_executor src/simple_single_threaded_executor.cpp)
ament_target_dependencies(simple_single_threaded_executor rclcpp std_msgs)

# Simple multi-threaded executor
add_executable(simple_multi_threaded_executor src/simple_multi_threaded_executor.cpp)
ament_target_dependencies(simple_multi_threaded_executor rclcpp std_msgs)

# Simple QoS publisher and subscriber
add_executable(simple_qos_publisher src/simple_qos_publisher.cpp)
ament_target_dependencies(simple_qos_publisher rclcpp std_msgs)

add_executable(simple_qos_subscriber src/simple_qos_subscriber.cpp)
ament_target_dependencies(simple_qos_subscriber rclcpp std_msgs)

# Manual composition example
add_executable(manual_composition src/manual_composition.cpp src/node1.cpp src/node2.cpp)
ament_target_dependencies(manual_composition rclcpp)

# Create a component library
add_library(number_publisher_component SHARED src/number_publisher_component.cpp)
ament_target_dependencies(number_publisher_component rclcpp rclcpp_components example_interfaces)
rclcpp_components_register_node(number_publisher_component PLUGIN "my_cpp_pkg::NumberPublisherComponent" 
                                                           EXECUTABLE number_publisher_component_exec)

# Install executables
install(TARGETS
  my_node
  simple_publisher
  simple_subscriber
  robot_news_station
  smart_phone
  number_publisher
  number_counter
  number_client
  number_publisher_lifecycle_node
  simple_service_server
  simple_service_client
  hw_status_publisher
  hw_status_subscriber
  led_panel
  battery
  simple_parameter
  simple_action_server
  simple_action_client
  count_until_server
  count_until_client
  count_until_server_queue_goals
  move_robot_server
  move_robot_client
  simple_lifecycle_node
  simple_single_threaded_executor
  simple_multi_threaded_executor
  simple_qos_publisher
  simple_qos_subscriber
  manual_composition
  DESTINATION lib/${PROJECT_NAME}
)

# Install the component library
install(TARGETS
  number_publisher_component
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

ament_package()
