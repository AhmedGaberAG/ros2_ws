from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    remap_topic = ("chatter", "qos_chatter")

    simple_qos_publisher_node = Node(
        package="my_py_pkg",
        executable="simple_qos_publisher",
        name="simple_qos_publisher",
        remappings=[
            remap_topic
        ]
    )

    simple_qos_subscriber_node = Node(
        package="my_py_pkg",
        executable="simple_qos_subscriber",
        name="simple_qos_subscriber",
        remappings=[
            remap_topic
        ]
    )

    ld.add_action(simple_qos_publisher_node)
    ld.add_action(simple_qos_subscriber_node)
    return ld
