from launch import LaunchDescription
from launch_ros.actions import LifecycleNode
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    number_node_name = "my_num_pub"

    number_publisher_lifecycle_node = LifecycleNode(
        package="my_py_pkg",
        executable="number_publisher_lifecycle_node",
        name=number_node_name,
        namespace=""
    )

    lifecycle_node_manager = Node(
        package="my_py_pkg",
        executable="lifecycle_node_manager",
        name="lifecycle_node_manager",
        parameters=[
            {"managed_node_name": number_node_name}
        ]
    )

    ld.add_action(number_publisher_lifecycle_node)
    ld.add_action(lifecycle_node_manager)
    return ld