import subprocess
import signal
import os
from pathlib import Path
from typing import List, Optional

class TelemetryRecorder:
    """Manages rosbag2 recording during a test run."""

    def __init__(self, topics: List[str], output_dir: Path):
        self.topics = topics
        self.output_dir = output_dir
        self.process: Optional[subprocess.Popen] = None
        self.bag_path = output_dir / "rosbag2"

    def start(self):
        """Start ros2 bag record process."""
        if not self.topics:
            print("⚠️  No topics specified, skipping recording.")
            return

        cmd = ["ros2", "bag", "record"] + self.topics + [
            "-o", str(self.bag_path),
            "--storage", "sqlite3"  # default, but explicit
        ]
        print(f"📹 Starting rosbag recording: {' '.join(cmd)}")

        # Start recording, redirect output to log files
        stdout_file = open(self.output_dir / "recorder_stdout.log", "w")
        stderr_file = open(self.output_dir / "recorder_stderr.log", "w")

        self.process = subprocess.Popen(
            cmd,
            stdout=stdout_file,
            stderr=stderr_file,
            text=True,
            preexec_fn=os.setsid,
            env=os.environ.copy()
        )

    def stop(self):
        """Stop the recording process."""
        if self.process:
            print("🛑 Stopping rosbag recording...")
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)
            self.process.wait()
            self.process = None
            print(f"✅ Rosbag saved to {self.bag_path}")