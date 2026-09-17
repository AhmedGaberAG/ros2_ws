from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    ld = LaunchDescription()
    robot_names = ["Giskard", "BB8", "Dannel", "Jander", "C3P0"]
    robot_news_station_nodes = [] 

    for name in robot_names:
        robot_news_station_nodes.append(Node(
            package="my_py_pkg",
            executable="robot_news_station",
            name="robot_news_station_" + name.lower(),
            parameters=[
                {"robot_name": name}
            ]
        ))

    smart_phone_node = Node(
        package="my_py_pkg",
        executable="smart_phone"
    )

    for node in robot_news_station_nodes:
        ld.add_action(node)
    ld.add_action(smart_phone_node)
    return ld
