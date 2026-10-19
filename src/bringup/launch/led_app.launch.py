from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()

    led_panel_node = Node(
        package="my_py_pkg",
        executable="led_panel",
        name="led_panel"
    )

    battery_node = Node(
        package="my_py_pkg",
        executable="battery",
        name="battery"
    )

    ld.add_action(led_panel_node)
    ld.add_action(battery_node)
    return ld
