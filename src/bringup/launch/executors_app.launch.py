from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    simple_single_threaded_executor_node = Node(
        package="my_py_pkg",
        executable="simple_single_threaded_executor",
        name="simple_single_threaded_executor"
    )

    simple_multi_threaded_executor_node = Node(
        package="my_py_pkg",
        executable="simple_multi_threaded_executor",
        name="simple_multi_threaded_executor"
    )

    ld.add_action(simple_single_threaded_executor_node)
    ld.add_action(simple_multi_threaded_executor_node)
    return ld
