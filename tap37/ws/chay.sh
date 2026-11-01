#!/bin/bash
# Chạy trong container ros-slam: robot giả lập + slam_toolbox, robot đi hết lộ trình thì tự dừng.
source /opt/ros/jazzy/setup.bash
rm -rf /ws/out && mkdir -p /ws/out
ros2 launch slam_toolbox online_async_launch.py slam_params_file:=/ws/slam.yaml use_sim_time:=false > /ws/out/slam.log 2>&1 &
SLAM=$!
sleep 4
python3 /ws/robot_gia.py
kill $SLAM 2>/dev/null
sleep 1
echo "--- nút đang chạy lúc cuối (từ log) ---"
grep -iE "loop|closure|error" /ws/out/slam.log | head -20
ls /ws/out | head
