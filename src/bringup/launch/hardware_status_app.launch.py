from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    hardware_status_publisher_node = Node(
        package="my_py_pkg",
        executable="hardware_status_publisher",
        name="hardware_status_publisher"
    )

    hardware_status_subscriber_node = Node(
        package="my_py_pkg",
        executable="hardware_status_subscriber",
        name="hardware_status_subscriber"
    )

    ld.add_action(hardware_status_publisher_node)
    ld.add_action(hardware_status_subscriber_node)
    return ld
