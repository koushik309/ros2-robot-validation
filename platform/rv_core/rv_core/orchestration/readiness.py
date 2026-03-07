import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile, DurabilityPolicy
import time

class ReadinessChecker(Node):
    """Checks if required topics are available."""

    def __init__(self, required_topics: list, timeout_sec: float = 30.0):
        super().__init__('readiness_checker')
        self.required_topics = required_topics
        self.timeout_sec = timeout_sec
        self.found_topics = set()

    def check(self) -> bool:
        """Wait for all required topics to appear."""
        start_time = time.time()
        while time.time() - start_time < self.timeout_sec:
            # Get list of all topics
            topic_names_and_types = self.get_topic_names_and_types()
            current_topics = {name for name, _ in topic_names_and_types}

            # Check which required topics are present
            for topic in self.required_topics:
                if topic in current_topics:
                    self.found_topics.add(topic)

            # If we have all, return success
            if self.found_topics.issuperset(self.required_topics):
                print(f"✅ All required topics found: {self.required_topics}")
                return True

            # Wait a bit before polling again
            time.sleep(1.0)

        # Timeout
        missing = set(self.required_topics) - self.found_topics
        print(f"❌ Timeout waiting for topics: {missing}")
        return False

def wait_for_topics(required_topics: list, timeout: float = 30.0) -> bool:
    """Convenience function to run readiness check."""
    rclpy.init()
    checker = ReadinessChecker(required_topics, timeout)
    success = checker.check()
    checker.destroy_node()
    rclpy.shutdown()
    return success