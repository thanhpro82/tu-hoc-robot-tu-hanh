#!/bin/bash
# Tập 1.7: chạy 3 node (robot, planner, controller) trong ROS 2 Jazzy và ghi lại output
source /opt/ros/jazzy/setup.bash
cd /ws
echo '$ ros2 run robot & planner'
python3 robot_node.py 2>&1 &
python3 planner_node.py 2>&1 &
sleep 4
echo '$ ros2 node list'
ros2 node list --spin-time 3
echo '$ ros2 topic list'
ros2 topic list
echo '$ python3 controller_node.py'
python3 controller_node.py 2>&1
