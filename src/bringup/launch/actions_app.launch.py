from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    simple_action_server_node = Node(
        package="my_py_pkg",
        executable="simple_action_server",
        name="simple_action_server"
    )

    count_until_server_node = Node(
        package="my_py_pkg",
        executable="count_until_server",
        name="count_until_server"
    )

    move_robot_server_node = Node(
        package="my_py_pkg",
        executable="move_robot_server",
        name="move_robot_server"
    )

    ld.add_action(simple_action_server_node)
    ld.add_action(count_until_server_node)
    ld.add_action(move_robot_server_node)
    return ld
