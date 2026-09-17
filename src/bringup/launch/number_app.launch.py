from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    remap_topic = ("number", "num")

    number_publisher_node = Node(
        package="my_py_pkg",
        executable="number_publisher",
        name="my_num_pub",
        remappings=[
            remap_topic
        ],
        parameters=[
            {"number": 2},
            {"frequency" : 1.0}
        ]
    )

    number_counter_node = Node(
        package="my_py_pkg",
        executable="number_counter",
        name="my_num_count",
        remappings=[
            remap_topic,
            ("number_count", "num_count")
        ]
    )

    number_subscriber_node = Node(
        package="my_py_pkg",
        executable="number_subscriber",
        name="my_num_sub", 
        remappings=[
            ("number_count", "num_count")
        ]
    )

    ld.add_action(number_publisher_node)
    ld.add_action(number_subscriber_node)
    ld.add_action(number_counter_node)
    return ld