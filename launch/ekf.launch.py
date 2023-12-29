import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory



def generate_launch_description():
    package_name='p0'
    robot_localization_file_path = os.path.join(get_package_share_directory(package_name), 'config/ekf.yaml') 

    return LaunchDescription([

        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[robot_localization_file_path]
        )
    ])
