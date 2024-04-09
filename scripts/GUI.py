#!/usr/bin/env python3
import tkinter as tk
import subprocess
from tkinter import messagebox
import time

class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal GUI")
        self.root.geometry("1000x600")
        self.root.configure(bg='#001F3F')

        self.processes = {"mapping": False, "navigation": False,"zone": False,"go": False,"deck": False}  # Dictionary to store process status (True for running, False for not running)

        self.commands = {
            # "mapping": ["ros2 launch p0 online_async_mapping_launch.py params_file:=/src/p0/config/mapper_params_online_async_mapping.yaml"],
            "mapping": ["ros2 launch p0 online_async_mapping_launch.py use_sim_time:=false"],
            "save_map": ["ros2 run nav2_map_server map_saver_cli -f ~/robot_ws/src/p0/scripts/map","ros2 service call /slam_toolbox/serialize_map slam_toolbox/srv/SerializePoseGraph 'filename: map'"],
            "delete_map": ["rm ~/robot_ws/src/p0/scripts/map.*"],
            # "navigation": ["ros2 launch p0 online_async_navigation_launch.py use_sim_time:=true","ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true"],
            "navigation": ["ros2 launch p0 online_async_navigation_launch.py use_sim_time:=false","ros2 launch p0 navigation_launch.py use_sim_time:=false"],#robot
            "zone": ["python3 path_planner.py"],
            "go": ["ros2 run p0 nav_through_poses.py"],
            "deck": ["ros2 run p0 nav_to_pose.py"],
            "robot_launch": ["ros2 launch p0 launch_robot.launch.py use_sim_time:=false"]#robot
            # "robot_launch": ["ros2 launch p0 launch_sim.launch.py use_sim_time:=true world:=~/robot_ws/src/p0/worlds/obstacles4.world"]
        }
        # Automatically start the launch_robot.launch.py process
        self.start_process("robot_launch")

        # Create other buttons excluding robot_launch
        self.create_buttons()

    def create_buttons(self):
        # Define coordinates for each button
        button_positions = {
            "mapping": (100, 100),
            "navigation": (400, 100),
            "zone": (700, 100),
            "go": (700, 250),
            "deck": (400, 250),
            "save_map": (100, 250),  # Position for save_map button
            "delete_map": (100, 400),  # Position for delete_map button
        }

        for process_key, command in self.commands.items():
            if process_key in button_positions:
                x, y = button_positions[process_key]
                button = tk.Button(self.root, text=process_key.capitalize(), command=lambda key=process_key: self.execute_command(key), height=5, width=20, bg='#4CAF50')  # Set initial color to green
                button.place(x=x, y=y)

                if process_key in ["mapping", "navigation", "zone", "go", "deck"]:
                    # Toggle buttons will change color when pressed
                    button.config(command=lambda key=process_key, b=button: self.toggle_button_color(b, key))

    def toggle_button_color(self, button, process_key):
        if self.processes[process_key]:
            button.configure(bg='#4CAF50')  # Set color to green when the process is running
        else:
            button.configure(bg='#FF5733')  # Set color to orange when the process is not running

        self.toggle_process(process_key)

    def execute_command(self, process_key):
        if process_key not in ["mapping", "navigation","zone","go","deck"]:
            self.start_process(process_key)

    def toggle_process(self, process_key):
        if self.processes[process_key]:
            self.kill_process(process_key)
        else:
            self.start_process(process_key)

    def start_process(self, process_key):
        try:
            # Kill existing processes with the same key
            self.kill_process(process_key)

            # Execute the new commands
            for command in self.commands[process_key]:
                subprocess.Popen(["x-terminal-emulator", "-e", command])
                time.sleep(6)  # Introduce a 5-second delay

            # Update process status to running
            self.processes[process_key] = True

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error executing commands: {e}")

    def kill_process(self, process_key):
        try:
            # Kill existing processes with the same key
            subprocess.run(["pkill", "-f", process_key])

            # Update process status to not running
            self.processes[process_key] = False

        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Error killing process: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = TerminalGUI(root)
    root.mainloop()
