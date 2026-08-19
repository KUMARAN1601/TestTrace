"""
Data models for TestTrace Recorder sessions and test steps.
"""
from datetime import datetime
from typing import Optional, List, Dict, Any
import uuid


class TestStep:
    """Represents a single test execution step with screenshot and metadata."""
    
    def __init__(self,
                 step_number: int,
                 timestamp: str = None,
                 screenshot_path: str = "",
                 annotated_path: str = "",
                 highlight_rect: Optional[Dict[str, int]] = None,
                 active_window: str = "",
                 click_position: Optional[Dict[str, int]] = None,
                 description: str = "",
                 result: str = "Untested"):
        """
        Initialize a test step.
        
        Args:
            step_number: Sequential step number in the test session
            timestamp: ISO format timestamp of capture
            screenshot_path: Path to raw screenshot file
            annotated_path: Path to annotated screenshot with highlights
            highlight_rect: Dictionary with x, y, w, h keys for highlight area
            active_window: Title of the active window during capture
            click_position: Dictionary with x, y keys for click coordinates
            description: Tester's description of the step action
            result: Step result - Pass, Fail, Blocked, or Untested
        """
        self.step_number = step_number
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.screenshot_path = screenshot_path
        self.annotated_path = annotated_path
        self.highlight_rect = highlight_rect or {}
        self.active_window = active_window
        self.click_position = click_position or {}
        self.description = description
        self.result = result
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert step to dictionary for JSON serialization."""
        return {
            "step_number": self.step_number,
            "timestamp": self.timestamp,
            "screenshot_path": self.screenshot_path,
            "annotated_path": self.annotated_path,
            "highlight_rect": self.highlight_rect,
            "active_window": self.active_window,
            "click_position": self.click_position,
            "description": self.description,
            "result": self.result
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestStep':
        """Create TestStep instance from dictionary."""
        return cls(
            step_number=data.get("step_number", 0),
            timestamp=data.get("timestamp", ""),
            screenshot_path=data.get("screenshot_path", ""),
            annotated_path=data.get("annotated_path", ""),
            highlight_rect=data.get("highlight_rect", {}),
            active_window=data.get("active_window", ""),
            click_position=data.get("click_position", {}),
            description=data.get("description", ""),
            result=data.get("result", "Untested")
        )


class TestSession:
    """Represents a complete test case execution session."""
    
    def __init__(self,
                 tc_id: str,
                 tc_name: str,
                 module: str,
                 environment: str,
                 tester_name: str,
                 session_id: str = None):
        """
        Initialize a test session.
        
        Args:
            tc_id: Test case identifier
            tc_name: Test case name/title
            module: Module or feature being tested
            environment: Testing environment
            tester_name: Name of the tester executing the test
            session_id: Unique session identifier (auto-generated if None)
        """
        self.session_id = session_id or str(uuid.uuid4())[:8]
        self.tc_id = tc_id
        self.tc_name = tc_name
        self.module = module
        self.environment = environment
        self.tester_name = tester_name
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.steps: List[TestStep] = []
    
    def add_step(self, step: TestStep) -> None:
        """Add a step to the session."""
        self.steps.append(step)
    
    def remove_step(self, step_number: int) -> bool:
        """Remove a step by its number. Returns True if removed."""
        for i, step in enumerate(self.steps):
            if step.step_number == step_number:
                self.steps.pop(i)
                self._renumber_steps()
                return True
        return False
    
    def _renumber_steps(self) -> None:
        """Renumber all steps sequentially after deletion or reordering."""
        for i, step in enumerate(self.steps, start=1):
            step.step_number = i
    
    def reorder_steps(self, old_index: int, new_index: int) -> None:
        """Move a step from old_index to new_index."""
        if 0 <= old_index < len(self.steps) and 0 <= new_index < len(self.steps):
            step = self.steps.pop(old_index)
            self.steps.insert(new_index, step)
            self._renumber_steps()
    
    def get_duration(self) -> str:
        """Get formatted session duration."""
        end = self.end_time or datetime.now()
        delta = end - self.start_time
        hours, remainder = divmod(int(delta.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def get_overall_status(self) -> str:
        """
        Determine overall test status based on step results.
        PASS only if all steps are Pass.
        """
        if not self.steps:
            return "NO STEPS"
        
        results = [step.result for step in self.steps]
        
        if "Fail" in results:
            return "FAIL"
        elif "Blocked" in results:
            return "BLOCKED"
        elif all(r == "Pass" for r in results):
            return "PASS"
        else:
            return "INCOMPLETE"
    
    def get_result_counts(self) -> Dict[str, int]:
        """Get counts of each result type."""
        counts = {"Pass": 0, "Fail": 0, "Blocked": 0, "Untested": 0}
        for step in self.steps:
            if step.result in counts:
                counts[step.result] += 1
        return counts
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert session to dictionary for JSON serialization."""
        return {
            "session_id": self.session_id,
            "tc_id": self.tc_id,
            "tc_name": self.tc_name,
            "module": self.module,
            "environment": self.environment,
            "tester_name": self.tester_name,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "steps": [step.to_dict() for step in self.steps]
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TestSession':
        """Create TestSession instance from dictionary."""
        session = cls(
            tc_id=data.get("tc_id", ""),
            tc_name=data.get("tc_name", ""),
            module=data.get("module", ""),
            environment=data.get("environment", ""),
            tester_name=data.get("tester_name", ""),
            session_id=data.get("session_id")
        )
        
        if data.get("start_time"):
            session.start_time = datetime.fromisoformat(data["start_time"])
        if data.get("end_time"):
            session.end_time = datetime.fromisoformat(data["end_time"])
        
        session.steps = [TestStep.from_dict(s) for s in data.get("steps", [])]
        
        return session
