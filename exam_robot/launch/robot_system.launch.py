from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import ExecuteProcess
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    urdf_path = os.path.join(
        get_package_share_directory('exam_robot'),
        'urdf',
        'exam_robot.urdf'
    )

    return LaunchDescription([
        # Robot State Publisher для публикации TF из URDF
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            output='screen',
            arguments=[urdf_path]
        ),

        # Наши узлы
        Node(
            package='exam_robot',
            executable='battery_node',
            name='battery_node',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='distance_sensor',
            name='distance_sensor',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen'
        ),
        Node(
            package='exam_robot',
            executable='status_display',
            name='status_display',
            output='screen'
        ),

        # Опционально: Joint State Publisher (если нужно публиковать joint_states вручную, но у нас уже есть в контроллере)
        # Node(
        #     package='joint_state_publisher',
        #     executable='joint_state_publisher',
        #     name='joint_state_publisher',
        #     arguments=[urdf_path]
        # ),
    ])