from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    simple_publisher_node = Node(
        package="my_cpp_pkg",
        executable="simple_publisher",
        name="simple_publisher"
    )

    simple_subscriber_node = Node(
        package="my_cpp_pkg",
        executable="simple_subscriber",
        name="simple_subscriber"
    )

    number_publisher_node = Node(
        package="my_cpp_pkg",
        executable="number_publisher",
        name="number_publisher",
        parameters=[
            {"number": 2}
        ]
    )

    number_counter_node = Node(
        package="my_cpp_pkg",
        executable="number_counter",
        name="number_counter"
    )

    robot_news_station_node = Node(
        package="my_cpp_pkg",
        executable="robot_news_station",
        name="robot_news_station",
        parameters=[
            {"robot_name": "R2D2"}
        ]
    )

    smart_phone_node = Node(
        package="my_cpp_pkg",
        executable="smart_phone",
        name="smart_phone"
    )

    hw_status_publisher_node = Node(
        package="my_cpp_pkg",
        executable="hw_status_publisher",
        name="hw_status_publisher"
    )

    hw_status_subscriber_node = Node(
        package="my_cpp_pkg",
        executable="hw_status_subscriber",
        name="hw_status_subscriber"
    )

    simple_service_server_node = Node(
        package="my_cpp_pkg",
        executable="simple_service_server",
        name="simple_service_server"
    )

    led_panel_node = Node(
        package="my_cpp_pkg",
        executable="led_panel",
        name="led_panel"
    )

    battery_node = Node(
        package="my_cpp_pkg",
        executable="battery",
        name="battery"
    )

    simple_action_server_node = Node(
        package="my_cpp_pkg",
        executable="simple_action_server",
        name="simple_action_server"
    )

    count_until_server_node = Node(
        package="my_cpp_pkg",
        executable="count_until_server",
        name="count_until_server"
    )

    move_robot_server_node = Node(
        package="my_cpp_pkg",
        executable="move_robot_server",
        name="move_robot_server"
    )

    simple_parameter_node = Node(
        package="my_cpp_pkg",
        executable="simple_parameter",
        name="simple_parameter"
    )

    simple_single_threaded_executor_node = Node(
        package="my_cpp_pkg",
        executable="simple_single_threaded_executor",
        name="simple_single_threaded_executor"
    )

    simple_multi_threaded_executor_node = Node(
        package="my_cpp_pkg",
        executable="simple_multi_threaded_executor",
        name="simple_multi_threaded_executor"
    )

    simple_lifecycle_node = Node(
        package="my_cpp_pkg",
        executable="simple_lifecycle_node",
        name="simple_lifecycle_node"
    )

    manual_composition_node = Node(
        package="my_cpp_pkg",
        executable="manual_composition",
        name="manual_composition"
    )

    ld.add_action(simple_publisher_node)
    ld.add_action(simple_subscriber_node)
    ld.add_action(number_publisher_node)
    ld.add_action(number_counter_node)
    ld.add_action(robot_news_station_node)
    ld.add_action(smart_phone_node)
    ld.add_action(hw_status_publisher_node)
    ld.add_action(hw_status_subscriber_node)
    ld.add_action(simple_service_server_node)
    ld.add_action(led_panel_node)
    ld.add_action(battery_node)
    ld.add_action(simple_action_server_node)
    ld.add_action(count_until_server_node)
    ld.add_action(move_robot_server_node)
    ld.add_action(simple_parameter_node)
    ld.add_action(simple_single_threaded_executor_node)
    ld.add_action(simple_multi_threaded_executor_node)
    ld.add_action(simple_lifecycle_node)
    ld.add_action(manual_composition_node)
    return ld
