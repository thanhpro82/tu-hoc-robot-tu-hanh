#!/bin/bash
# Kịch bản demo tập 0.3: chạy robot_node.py rồi dùng các lệnh ros2 để xem node/topic
source /opt/ros/jazzy/setup.bash
cd /ws
echo '$ python3 robot_node.py &'
python3 robot_node.py 2>&1 &
sleep 3
echo '$ ros2 node list'
ros2 node list
echo '$ ros2 topic list'
ros2 topic list
echo '$ ros2 topic pub /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 1.0}}"'
ros2 topic pub --rate 10 /cmd_vel geometry_msgs/msg/Twist "{linear: {x: 0.5}, angular: {z: 1.0}}" > /dev/null &
sleep 3
echo '$ ros2 topic echo /pose --once'
ros2 topic echo /pose --once
sleep 1.5
echo '$ ros2 topic echo /pose --once'
ros2 topic echo /pose --once
