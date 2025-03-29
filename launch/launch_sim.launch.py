import os

from ament_index_python.packages import get_package_share_directory


from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node

import xacro


def generate_launch_description():



    package_name='humblebot' 
    file_subpath = 'description/robot.urdf.xacro'

    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    xacro_file = os.path.join(get_package_share_directory(package_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
        'use_sim_time': True}] # add other parameters here if required
    )
    
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
             )

    spawn_entity = Node(
    package='gazebo_ros',
    executable='spawn_entity.py',
    arguments=[
        '-topic', 'robot_description',
        '-entity', 'humblebot',
        '-x', '0',
        '-y', '0',
        '-z', '0.05'  
    ],
    output='screen'
)




    return LaunchDescription([
        rsp,
        gazebo,
        spawn_entity,
    ])
