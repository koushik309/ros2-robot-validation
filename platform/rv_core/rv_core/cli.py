import os
import sys
import time
import yaml
import click
from .spec import TestSpec
from .utils import create_run_dir, save_spec_copy
from .orchestration.sim_launcher import SimulationLauncher
from .orchestration.readiness import wait_for_topics
from .telemetry.recorder import TelemetryRecorder

@click.group()
def cli():
    """ROS2 Robot Validation Toolkit CLI."""
    pass

@cli.command()
@click.argument('spec_file', type=click.Path(exists=True))
def run(spec_file):
    """Run a validation test from a YAML spec file."""
    # Load spec
    spec = TestSpec.from_yaml(spec_file)
    click.echo(f"✅ Spec loaded: {spec.robot.name} in {spec.run.mode} mode")
    click.echo(f"   Duration: {spec.run.duration_s}s")
    click.echo(f"   Tests: {[t.id for t in spec.tests]}")

    # Determine recording topics from spec (if telemetry enabled)
    recording_topics = []
    if spec.telemetry and spec.telemetry.record_rosbag:
        recording_topics = spec.telemetry.topics
        click.echo(f"📹 Telemetry enabled, recording topics: {recording_topics}")
    else:
        click.echo("📹 Telemetry not enabled (no topics will be recorded)")

    # Create run directory
    run_dir = create_run_dir()
    click.echo(f"📁 Run directory: {run_dir}")

    # Create log subdirectory
    log_dir = run_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    # Save a copy of the spec
    with open(spec_file, 'r') as f:
        spec_dict = yaml.safe_load(f)
    save_spec_copy(spec_dict, run_dir)

    # Handle simulation mode
    if spec.run.mode == "sim":
        # Launch simulation
        launcher = SimulationLauncher(spec.robot.name)
        try:
            launcher.start(log_dir)  # pass log_dir
            click.echo("⏳ Waiting for simulation to start...")
            time.sleep(15)  # increased from 5

            # Optional: dump current topics for debugging
            import subprocess
            result = subprocess.run(["ros2", "topic", "list"], capture_output=True, text=True)
            click.echo(f"📋 Topics currently visible: {result.stdout}")

            # Readiness check
            required_topics = ['/joint_states', '/tf']
            click.echo(f"🔍 Checking for topics: {required_topics}")
            if not wait_for_topics(required_topics, timeout=30):
                click.echo("❌ Simulation did not become ready. Aborting.")
                launcher.stop()
                sys.exit(1)

            click.echo("✅ Simulation is ready.")

            # Start telemetry recording if topics are provided
            recorder = None
            if recording_topics:
                recorder = TelemetryRecorder(recording_topics, run_dir)
                recorder.start()
            else:
                click.echo("⏩ No topics to record, skipping rosbag.")

            click.echo(f"⏳ Simulating test run for {spec.run.duration_s} seconds...")
            time.sleep(spec.run.duration_s)

            if recorder:
                recorder.stop()

        finally:
            launcher.stop()

    elif spec.run.mode == "replay":
        click.echo("🔁 Replay mode not yet implemented.")
    elif spec.run.mode == "hil":
        click.echo("🛠️ HIL mode not yet implemented.")
    else:
        click.echo(f"❌ Unknown mode: {spec.run.mode}")

    click.echo(f"✅ Test run completed. Check artifacts in {run_dir}")

def main():
    cli()

if __name__ == '__main__':
    main()