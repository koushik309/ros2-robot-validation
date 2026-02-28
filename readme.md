# ROS2 Robot Test & Validation Toolkit

**Framework for repeatable validation tests on ROS2 robots (simulation + real hardware) with auditable reports.**

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/)
[![ROS2](https://img.shields.io/badge/ROS2-Humble/Iron/Jazzy-blue)](https://docs.ros.org/)

## Why This Toolkit?

Robotics development needs confidence that changes don’t break existing behavior. This toolkit provides:

- **Repeatability** – Same test, same results (within tolerance)
- **Traceability** – Logs, configs, and artifacts saved per run
- **Coverage** – Motion, sensors, safety, performance, communication
- **Automated Reporting** – HTML/PDF reports with plots and pass/fail verdicts

## Features

- **Test Packs (plugins):**
  - Motion & kinematics validation (repeatability, trajectory accuracy, backlash)
  - Controller performance (latency, jitter, step response)
  - Sensor sanity (encoder consistency, IMU drift, lidar scan rate)
  - System reliability (node lifecycle, topic availability, CPU/memory)
  - Safety (E‑stop response, safe speed zones, collision stop)

- **Run Modes:**
  - `sim` – Gazebo/Ignition with fake controllers
  - `hil` – Real robot over ROS2 drivers with safety gating
  - `replay` – Re-run metrics on recorded rosbag2 files

- **Artifacts per Run:**
  - Full test specification (YAML)
  - rosbag2 with all relevant topics
  - System info & ROS graph dump
  - Metrics & verdict JSON
  - Interactive HTML report with plots

## Quick Start (Simulation)

### Prerequisites
- ROS 2 **Jazzy**, Humble, or Iron (with `ros2_control`, `gazebo`)
  *Note: Jazzy is an older, but still supported, LTS distribution.*
- Python 3.8+ with `pip`

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ros2-robot-validation.git
cd ros2-robot-validation

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the core package
pip install -e platform/rv_core


