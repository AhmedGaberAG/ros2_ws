import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    ld = LaunchDescription()

    launch_dir = os.path.join(get_package_share_directory("bringup"), "launch")

    app_files = [
        "python_app.launch.py",
        "number_app.launch.py",
        "radio_app.launch.py"
    ]

    for app_file in app_files:
        ld.add_action(IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(launch_dir, app_file))
        ))

    return ld
