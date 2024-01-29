## Robot Package Template

This is a GitHub template. You can make your own copy by clicking the green "Use this template" button.

It is recommended that you keep the repo/package name the same, but if you do change it, ensure you do a "Find all" using your IDE (or the built-in GitHub IDE by hitting the `.` key) and rename all instances of `p0` to whatever your project's name is.

Note that each directory currently has at least one file in it to ensure that git tracks the files (and, consequently, that a fresh clone has direcctories present for CMake to find). These example files can be removed if required (and the directories can be removed if `CMakeLists.txt` is adjusted accordingly).

 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

Required packages for runing this code:

https://github.com/joshnewans/diffdrive_arduino.git

https://github.com/joshnewans/ball_tracker.git

https://github.com/joshnewans/serial.git

https://github.com/flynneva/bno055.git

https://github.com/ldrobotSensorTeam/ldlidar_stl_ros2.git


ros2 run tf2_tools view_frames.py
rqt_graph
killall gzserver
ros2 launch slam_toolbox online_async_launch.py params_file:=./src/p0/config/mapper_params_online_async.yaml use_sim_time:=true
ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true