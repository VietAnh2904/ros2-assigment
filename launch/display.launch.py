import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'robot_final'
    
    # 1. Đường dẫn tới file URDF
    urdf_file = os.path.join(get_package_share_directory(package_name), 'urdf', 'robot_final.urdf')

    # 2. Đọc nội dung file URDF
    with open(urdf_file, 'r') as infp:
        robot_description_config = infp.read()

    return LaunchDescription([
        # Node phát tọa độ robot
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': robot_description_config, # Khớp tên biến
                'publish_frequency': 50.0 # Tần số cao để hết ảo ảnh
            }]
        ),
        # Node hiện thanh trượt
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),
        # Node mở RViz2
        Node(
            package='rviz2',
            executable='rviz2'
        )
    ])
