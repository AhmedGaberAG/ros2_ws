from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    simple_parameter_node = Node(
        package="my_py_pkg",
        executable="simple_parameter",
        name="simple_parameter"
    )

    ld.add_action(simple_parameter_node)
    return ld
