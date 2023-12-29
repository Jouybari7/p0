import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():

    return LaunchDescription([
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(os.path.join(os.path.dirname(__file__), 'ld19.launch.py')),
            launch_arguments={'serial_port': '/dev/serial/by-path/platform-70090000.xusb-usb-0:2.2:1.0-port0',
                              'frame_id': 'laser_frame',
                              'angle_compensate': 'True',
                              'scan_mode': 'Standard'}.items(),
        ),
    ])
