from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    container_node = Node(
        package="my_py_pkg",
        executable="container",
        name="container"
    )

    ld.add_action(container_node)
    return ld
