#! /usr/bin/env python3
# Copyright 2021 Samsung Research America
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator, TaskResult
import rclpy
from rclpy.duration import Duration
import os
import math
"""
Basic navigation demo to go to poses.
"""
file_path = os.path.expanduser('~/robot_ws/src/p0/scripts/poses.txt')

# def read_poses_from_file(file_path):
    # poses = []
    # with open(file_path, 'r') as file:
    #     x_prv=0
    #     y_prv=0
    #     goal_poses = []
    #     for line in file:
    #         # Strip square brackets and split the line into x and y values
    #         values = line.strip().strip('[]').split()
    #         # Convert x and y values to float
    #         x, y = map(float, values)
    #         half_angle=math.atan2((x-x_prv), (y-y_prv))/2
    #         # quaternion.z = math.sin(half_angle)  # z-component of the axis of rotation
    #         # quaternion.w = math.cos(half_angle)  # scalar part (cosine of half angle)
    #         x_prv=x
    #         y_prv=y  
    #         goal_pose1 = PoseStamped()
    #         goal_pose1.header.frame_id = 'map'
    #         goal_pose1.header.stamp = navigator.get_clock().now().to_msg()
    #         goal_pose1.pose.position.x = x
    #         goal_pose1.pose.position.y = y
    #         goal_pose1.pose.orientation.w = math.cos(half_angle)
    #         goal_pose1.pose.orientation.z = math.sin(half_angle)
    #         goal_poses.append(goal_pose1)
    #                 # poses.append([x, y])
    #         print(goal_pose1)
    #         return goal_poses



def main():
    # poses = read_poses_from_file(file_path)
    rclpy.init()

    navigator = BasicNavigator()

    # Set our demo's initial pose
    initial_pose = PoseStamped()
    initial_pose.header.frame_id = 'map'
    initial_pose.header.stamp = navigator.get_clock().now().to_msg()
    initial_pose.pose.position.x = 0.0
    initial_pose.pose.position.y = 0.0
    initial_pose.pose.orientation.z = 0.0
    initial_pose.pose.orientation.w = 0.0
    navigator.setInitialPose(initial_pose)

    # Activate navigation, if not autostarted. This should be called after setInitialPose()
    # or this will initialize at the origin of the map and update the costmap with bogus readings.
    # If autostart, you should `waitUntilNav2Active()` instead.
    # navigator.lifecycleStartup()

    # Wait for navigation to fully activate, since autostarting nav2
    # navigator.waitUntilNav2Active()

    # If desired, you can change or load the map as well
    # navigator.changeMap('/path/to/map.yaml')

    # You may use the navigator to clear or obtain costmaps
    # navigator.clearAllCostmaps()  # also have clearLocalCostmap() and clearGlobalCostmap()
    # global_costmap = navigator.getGlobalCostmap()
    # local_costmap = navigator.getLocalCostmap()

    # set our demo's goal poses
    goal_poses = []
    with open(file_path, 'r') as file:
        x_prv=0
        y_prv=0
        for line in file:
            # Strip square brackets and split the line into x and y values
            values = line.strip().strip('[]').split()
            # Convert x and y values to float
            x, y = map(float, values)
            half_angle=math.atan2((x-x_prv), (y-y_prv))/2
            # quaternion.z = math.sin(half_angle)  # z-component of the axis of rotation
            # quaternion.w = math.cos(half_angle)  # scalar part (cosine of half angle)
            x_prv=x
            y_prv=y  
            goal_pose1 = PoseStamped()
            goal_pose1.header.frame_id = 'map'
            goal_pose1.header.stamp = navigator.get_clock().now().to_msg()
            goal_pose1.pose.position.x = x
            goal_pose1.pose.position.y = y
            goal_pose1.pose.orientation.w = round(math.cos(half_angle),3)
            goal_pose1.pose.orientation.z = round(math.sin(half_angle),3)
            goal_poses.append(goal_pose1)
            print("  Position (x, y):", goal_pose1.pose.position.x, goal_pose1.pose.position.y)
            print("  Orientation (w, z):", goal_pose1.pose.orientation.w, goal_pose1.pose.orientation.z)

                    # poses.append([x, y])
            # print(goal_pose1)


    # additional goals can be appended
    # goal_pose2 = PoseStamped()
    # goal_pose2.header.frame_id = 'map'
    # goal_pose2.header.stamp = navigator.get_clock().now().to_msg()
    # goal_pose2.pose.position.x = 0.0
    # goal_pose2.pose.position.y = 0.0
    # goal_pose2.pose.orientation.w = 0.707
    # goal_pose2.pose.orientation.z = 0.707
    # goal_poses.append(goal_pose2)
    # goal_pose3 = PoseStamped()
    # goal_pose3.header.frame_id = 'map'
    # goal_pose3.header.stamp = navigator.get_clock().now().to_msg()
    # goal_pose3.pose.position.x = -3.6
    # goal_pose3.pose.position.y = -4.75
    # goal_pose3.pose.orientation.w = 0.707
    # goal_pose3.pose.orientation.z = 0.707
    # goal_poses.append(goal_pose3)

    # sanity check a valid path exists
    # path = navigator.getPathThroughPoses(initial_pose, goal_poses)

    navigator.goThroughPoses(goal_poses)

    i = 0
    while not navigator.isTaskComplete():
        ################################################
        #
        # Implement some code here for your application!
        #
        ################################################

        # Do something with the feedback
        i = i + 1
        feedback = navigator.getFeedback()
        if feedback and i % 5 == 0:
            print(
                'Estimated time of arrival: '
                + '{0:.0f}'.format(
                    Duration.from_msg(feedback.estimated_time_remaining).nanoseconds
                    / 1e9
                )
                + ' seconds.'
            )

            # Some navigation timeout to demo cancellation
            # if Duration.from_msg(feedback.navigation_time) > Duration(seconds=600.0):
            #     navigator.cancelTask()

            # Some navigation request change to demo preemption
            # if Duration.from_msg(feedback.navigation_time) > Duration(seconds=35.0):
            #     goal_pose4 = PoseStamped()
            #     goal_pose4.header.frame_id = 'map'
            #     goal_pose4.header.stamp = navigator.get_clock().now().to_msg()
            #     goal_pose4.pose.position.x = -5.0
            #     goal_pose4.pose.position.y = -4.75
            #     goal_pose4.pose.orientation.w = 0.707
            #     goal_pose4.pose.orientation.z = 0.707
            #     navigator.goThroughPoses([goal_pose4])

    # Do something depending on the return code
    result = navigator.getResult()
    if result == TaskResult.SUCCEEDED:
        print('Goal succeeded!')
    elif result == TaskResult.CANCELED:
        print('Goal was canceled!')
    elif result == TaskResult.FAILED:
        print('Goal failed!')
    else:
        print('Goal has an invalid return status!')

    # navigator.lifecycleShutdown()

    exit(0)


if __name__ == '__main__':
    main()