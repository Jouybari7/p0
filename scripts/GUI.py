import tkinter as tk
import subprocess
from tkinter import messagebox

class TerminalGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Terminal GUI")
        self.root.geometry("800x600")
        self.root.configure(bg='#001F3F')

        self.processes = {"map": False, "navigate": False}  # Dictionary to store process status (True for running, False for not running)

        self.commands = {
            "map": ["ros2 launch p0 online_async_launch.py params_file:=/src/p0/config/mapper_params_online_async_mapping.yaml"],
            "save_map": ["ros2 run nav2_map_server map_saver_cli -f ~/robot_ws/src/p0/map/map"],
            "delete_map": ["rm ~/robot_ws/src/p0/map/map.*"],
            "navigate": [
                "echo 'Command 4.1 executed'",
                "echo 'Command 4.2 executed'",
                "echo 'Command 4.3 executed'"
            ],
            "rc_mode": ["ros2 launch p0 launch_robot.launch.py"]
        }

        # Automatically start the launch_robot.launch.py process
        self.start_process("rc_mode")

        # Create other buttons excluding rc_mode
        self.create_buttons()

    def create_buttons(self):
        for process_key, command in self.commands.items():
            if process_key != "rc_mode":
                button = tk.Button(self.root, text=process_key.capitalize(), command=lambda key=process_key: self.execute_command(key), height=5, width=20, bg='#4CAF50')  # Set initial color to green
                button.pack(pady=10)

                if process_key in ["map", "navigate"]:
                    # Toggle buttons will change color when pressed
                    button.config(command=lambda key=process_key, b=button: self.toggle_button_color(b, key))

    def toggle_button_color(self, button, process_key):
        if self.processes[process_key]:
            button.configure(bg='#4CAF50')  # Set color to green when the process is running
        else:
            button.configure(bg='#FF5733')  # Set color to orange when the process is not running

        self.toggle_process(process_key)

    def execute_command(self, process_key):
        if process_key not in ["map", "navigate"]:
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
