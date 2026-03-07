import subprocess
import time
import signal
import os
from pathlib import Path
from typing import Optional

class SimulationLauncher:
    """Launches and manages a Gazebo simulation process."""

    def __init__(self, robot_name: str, world: str = "empty"):
        self.robot_name = robot_name
        self.world = world
        self.process: Optional[subprocess.Popen] = None

        # Map robot names to actual launch commands
        # For now, we hardcode a few common examples.
        # Later this could be extended via configuration or adapters.
        self.launch_commands = {
            "rrbot": [
                "ros2", "launch", "ros2_control_demo_example_1", "rrbot.launch.py"
            ],
            "turtlebot3": [
                "ros2", "launch", "turtlebot3_gazebo", "turtlebot3_world.launch.py"
            ],
            # Add more as needed
        }

    def start(self, log_dir: Path) -> bool:
        """Launch the simulation process and redirect logs."""
        if self.robot_name not in self.launch_commands:
            raise ValueError(f"Unknown robot: {self.robot_name}. Available: {list(self.launch_commands.keys())}")

        cmd = self.launch_commands[self.robot_name]
        print(f"🚀 Launching simulation for {self.robot_name}: {' '.join(cmd)}")

        # Open log files
        stdout_file = open(log_dir / "sim_stdout.log", "w")
        stderr_file = open(log_dir / "sim_stderr.log", "w")

        my_env = os.environ.copy()
        my_env["LIBGL_ALWAYS_SOFTWARE"] = "1"

        self.process = subprocess.Popen(
            cmd,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
            preexec_fn=os.setsid,
            env=os.environ.copy()
        )
        return True
    def stop(self):
        """Terminate the simulation process."""
        if self.process:
            print("🛑 Stopping simulation...")
            # Kill the entire process group
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait()
            self.process = None

    def is_running(self) -> bool:
        """Check if process is still alive."""
        if self.process is None:
            return False
        return self.process.poll() is None