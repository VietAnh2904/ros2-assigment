import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess, TimerAction
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    package_name = 'robot_final'
    pkg_share = get_package_share_directory(package_name)
    urdf_file = os.path.join(pkg_share, 'urdf', 'robot_final.urdf')

    # 1. Node Robot State Publisher
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': open(urdf_file).read(), 'use_sim_time': True}]
    )

    # 2. Node Joint State Publisher (Cần thiết để hiện TF cảm biến)
    joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
        parameters=[{'use_sim_time': True}]
    )

    # 3. Mở Gazebo
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    )

    # 4. Thả robot vào Gazebo
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'my_robot'],
        output='screen'
    )

    # 5. MỞ RVIZ2
    rviz = Node(
        package='rviz2',
        executable='rviz2',
        parameters=[{'use_sim_time': True}]
    )

    # 6. TỰ ĐỘNG MỞ TERMINAL ĐIỀU KHIỂN
    teleop_terminal = TimerAction(
        period=5.0,
        actions=[
            ExecuteProcess(
                cmd=['gnome-terminal', '--', 'ros2', 'run', 'teleop_twist_keyboard', 'teleop_twist_keyboard'],
                output='screen'
            )
        ]
    )

    return LaunchDescription([
        robot_state_publisher,
        joint_state_publisher,
        gazebo,
        spawn_entity,
        rviz,
        teleop_terminal
    ])
