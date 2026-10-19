from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    simple_service_server_node = Node(
        package="my_py_pkg",
        executable="simple_service_server",
        name="simple_service_server"
    )

    compute_rectangle_area_server_node = Node(
        package="my_py_pkg",
        executable="compute_rectangle_area_server",
        name="compute_rectangle_area_server"
    )

    ld.add_action(simple_service_server_node)
    ld.add_action(compute_rectangle_area_server_node)
    return ld
