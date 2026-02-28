from pydantic import BaseModel, Field
from typing import List, Optional, Any
import yaml

class RunConfig(BaseModel):
    mode: str = Field(..., description="sim, hil, or replay")
    duration_s: Optional[float] = 10.0

class RobotConfig(BaseModel):
    name: str
    urdf: Optional[str] = None
    joints: List[str] = []

class TestItem(BaseModel):
    id: str
    params: dict[str, Any] = {}
    thresholds: dict[str, Any] = {}

class TestSpec(BaseModel):
    run: RunConfig
    robot: RobotConfig
    tests: List[TestItem] = []

    @classmethod
    def from_yaml(cls, path: str):
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
        return cls(**data)