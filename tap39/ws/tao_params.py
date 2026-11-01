"""Tập 3.9: tạo nav2.yaml từ file tham số mặc định của nav2_bringup, chỉ sửa những chỗ cần cho robot giả lập."""
import yaml

p = yaml.safe_load(open("nav2_goc.yaml", encoding="utf8").read().replace("base_footprint", "base_link"))
a = p["amcl"]["ros__parameters"]
a.update(laser_max_range=8.0, laser_min_range=0.1, set_initial_pose=False)
# LiDAR giả lập rất chuẩn (σ 1 cm) và odometry khá tốt: tin cảm biến hơn mặc định (z_hit 0,5 / z_rand 0,5, alpha 0,2)
a.update(z_hit=0.9, z_rand=0.1, sigma_hit=0.1, alpha1=0.05, alpha2=0.05, alpha3=0.05, alpha4=0.05)
c = p["controller_server"]["ros__parameters"]
c["general_goal_checker"]["xy_goal_tolerance"] = 0.10   # mặc định 0,25 m
c["FollowPath"] = {   # bám đường kiểu pure pursuit: nhìn trước một điểm trên đường rồi lái về phía đó
    "plugin": "nav2_regulated_pure_pursuit_controller::RegulatedPurePursuitController",
    "desired_linear_vel": 0.45, "lookahead_dist": 0.6, "min_lookahead_dist": 0.3, "max_lookahead_dist": 0.9,
    "lookahead_time": 1.5, "use_velocity_scaled_lookahead_dist": False, "transform_tolerance": 0.1,
    "min_approach_linear_velocity": 0.05, "approach_velocity_scaling_dist": 0.6,
    "use_collision_detection": True, "max_allowed_time_to_collision_up_to_carrot": 1.0,
    "use_regulated_linear_velocity_scaling": True, "use_cost_regulated_linear_velocity_scaling": False,
    "regulated_linear_scaling_min_radius": 0.9, "regulated_linear_scaling_min_speed": 0.25,
    "use_rotate_to_heading": True, "rotate_to_heading_angular_vel": 1.2, "rotate_to_heading_min_angle": 0.785,
    "max_angular_accel": 3.2, "allow_reversing": False, "max_robot_pose_search_dist": 10.0,
}
for k in ("local_costmap", "global_costmap"):
    q = p[k][k]["ros__parameters"]
    q["robot_radius"] = 0.2
    q["inflation_layer"]["inflation_radius"] = 0.55
p["local_costmap"]["local_costmap"]["ros__parameters"].update(width=4, height=4)
p["planner_server"]["ros__parameters"]["GridBased"]["use_astar"] = False  # Dijkstra (mặc định). Đã thử A*: 45,3 s, 16,31 m, 1 lần phục hồi -> giữ Dijkstra
yaml.safe_dump(p, open("nav2.yaml", "w", encoding="utf8"), sort_keys=False, allow_unicode=True)
print("ok nav2.yaml")
