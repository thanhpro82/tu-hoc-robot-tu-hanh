#!/bin/bash
# Chạy trong container ros-nav: robot giả lập + Nav2 (map_server, AMCL, planner, controller...) trên bản đồ tập 3.7,
# rồi ra lệnh đi tới bếp. Xong thì tự tắt.
source /opt/ros/jazzy/setup.bash
rm -rf /ws/out && mkdir -p /ws/out
python3 /ws/robot_nav.py > /ws/out/robot.log 2>&1 &
ROBOT=$!
sleep 2
ros2 launch nav2_bringup bringup_launch.py map:=/ws/map/nha.yaml params_file:=/ws/nav2.yaml use_sim_time:=False autostart:=True > /ws/out/nav2.log 2>&1 &
NAV=$!
sleep 6
timeout 400 python3 /ws/ra_lenh.py
kill $NAV $ROBOT 2>/dev/null
sleep 2
grep -iE "error|fail|abort|replan|recover" /ws/out/nav2.log | grep -v "Failed to get" | head -30
tail -1 /ws/out/robot.jsonl
