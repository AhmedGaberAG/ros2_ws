from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    simple_publisher_node = Node(
        package="my_py_pkg",
        executable="simple_publisher",
        name="simple_publisher"
    )

    simple_subscriber_node = Node(
        package="my_py_pkg",
        executable="simple_subscriber",
        name="simple_subscriber"
    )

    ld.add_action(simple_publisher_node)
    ld.add_action(simple_subscriber_node)
    return ld
