import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    ld = LaunchDescription()

    launch_dir = os.path.join(get_package_share_directory("bringup"), "launch")

    app_files = [
        "chatter_app.launch.py",
        "hardware_status_app.launch.py",
        "services_app.launch.py",
        "led_app.launch.py",
        "actions_app.launch.py",
        "parameters_app.launch.py",
        "qos_app.launch.py",
        "executors_app.launch.py",
        "composition_app.launch.py",
        "lifecycle_app.launch.py"
    ]

    for app_file in app_files:
        ld.add_action(IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, app_file))
        ))

    return ld
