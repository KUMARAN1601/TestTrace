"""
Unit tests for session_model.py - TestStep and TestSession classes.
"""
import pytest
from datetime import datetime
from session_model import TestStep, TestSession


class TestTestStep:
    """Test cases for TestStep class."""
    
    def test_step_initialization_with_defaults(self):
        """Test TestStep creation with default values."""
        step = TestStep(step_number=1)
        
        assert step.step_number == 1
        assert step.timestamp is not None
        assert step.screenshot_path == ""
        assert step.annotated_path == ""
        assert step.highlight_rect == {}
        assert step.active_window == ""
        assert step.click_position == {}
        assert step.description == ""
        assert step.result == "Untested"
    
    def test_step_initialization_with_all_fields(self):
        """Test TestStep creation with all fields specified."""
        timestamp = "2026-08-19 10:30:45"
        highlight = {"x": 100, "y": 200, "w": 300, "h": 150}
        click_pos = {"x": 250, "y": 275}
        
        step = TestStep(
            step_number=5,
            timestamp=timestamp,
            screenshot_path="/path/to/screenshot.png",
            annotated_path="/path/to/annotated.png",
            highlight_rect=highlight,
            active_window="Chrome - Test Page",
            click_position=click_pos,
            description="Clicked Submit button",
            result="Pass"
        )
        
        assert step.step_number == 5
        assert step.timestamp == timestamp
        assert step.screenshot_path == "/path/to/screenshot.png"
        assert step.annotated_path == "/path/to/annotated.png"
        assert step.highlight_rect == highlight
        assert step.active_window == "Chrome - Test Page"
        assert step.click_position == click_pos
        assert step.description == "Clicked Submit button"
        assert step.result == "Pass"
    
    def test_step_to_dict(self):
        """Test TestStep serialization to dictionary."""
        step = TestStep(
            step_number=3,
            timestamp="2026-08-19 10:30:45",
            screenshot_path="/test.png",
            description="Test step",
            result="Fail"
        )
        
        step_dict = step.to_dict()
        
        assert isinstance(step_dict, dict)
        assert step_dict["step_number"] == 3
        assert step_dict["timestamp"] == "2026-08-19 10:30:45"
        assert step_dict["screenshot_path"] == "/test.png"
        assert step_dict["description"] == "Test step"
        assert step_dict["result"] == "Fail"
    
    def test_step_from_dict(self):
        """Test TestStep deserialization from dictionary."""
        data = {
            "step_number": 7,
            "timestamp": "2026-08-19 11:00:00",
            "screenshot_path": "/screen.png",
            "annotated_path": "/screen_annotated.png",
            "highlight_rect": {"x": 50, "y": 60, "w": 100, "h": 80},
            "active_window": "Notepad",
            "click_position": {"x": 100, "y": 100},
            "description": "Typed text",
            "result": "Pass"
        }
        
        step = TestStep.from_dict(data)
        
        assert step.step_number == 7
        assert step.timestamp == "2026-08-19 11:00:00"
        assert step.screenshot_path == "/screen.png"
        assert step.annotated_path == "/screen_annotated.png"
        assert step.highlight_rect == {"x": 50, "y": 60, "w": 100, "h": 80}
        assert step.active_window == "Notepad"
        assert step.click_position == {"x": 100, "y": 100}
        assert step.description == "Typed text"
        assert step.result == "Pass"
    
    def test_step_roundtrip_serialization(self):
        """Test that step survives to_dict -> from_dict conversion."""
        original = TestStep(
            step_number=10,
            description="Original step",
            result="Blocked"
        )
        
        step_dict = original.to_dict()
        restored = TestStep.from_dict(step_dict)
        
        assert restored.step_number == original.step_number
        assert restored.description == original.description
        assert restored.result == original.result


class TestTestSession:
    """Test cases for TestSession class."""
    
    def test_session_initialization(self):
        """Test TestSession creation with required fields."""
        session = TestSession(
            tc_id="TC_001",
            tc_name="Test Login Flow",
            module="Authentication",
            environment="SIT",
            tester_name="John Doe"
        )
        
        assert session.tc_id == "TC_001"
        assert session.tc_name == "Test Login Flow"
        assert session.module == "Authentication"
        assert session.environment == "SIT"
        assert session.tester_name == "John Doe"
        assert session.session_id is not None
        assert len(session.session_id) == 8
        assert isinstance(session.start_time, datetime)
        assert session.end_time is None
        assert session.steps == []
    
    def test_session_with_optional_fields(self):
        """Test TestSession with custom session_id."""
        session = TestSession(
            tc_id="TC_002",
            tc_name="Test Payment",
            module="Payment",
            environment="UAT",
            tester_name="Jane Smith",
            session_id="custom99"
        )
        
        assert session.session_id == "custom99"
    
    def test_session_custom_id(self):
        """Test TestSession with custom session_id."""
        session = TestSession(
            tc_id="TC_003",
            tc_name="Test",
            module="Module",
            environment="Dev",
            tester_name="Tester",
            session_id="custom99"
        )
        
        assert session.session_id == "custom99"
    
    def test_add_step(self):
        """Test adding steps to a session."""
        session = TestSession(
            tc_id="TC_004",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        step1 = TestStep(step_number=1, description="First step")
        step2 = TestStep(step_number=2, description="Second step")
        
        session.add_step(step1)
        session.add_step(step2)
        
        assert len(session.steps) == 2
        assert session.steps[0].description == "First step"
        assert session.steps[1].description == "Second step"
    
    def test_remove_step(self):
        """Test removing a step by number."""
        session = TestSession(
            tc_id="TC_005",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        session.add_step(TestStep(step_number=1, description="Step 1"))
        session.add_step(TestStep(step_number=2, description="Step 2"))
        session.add_step(TestStep(step_number=3, description="Step 3"))
        
        result = session.remove_step(2)
        
        assert result is True
        assert len(session.steps) == 2
        assert session.steps[0].step_number == 1
        assert session.steps[1].step_number == 2  # Renumbered from 3
        assert session.steps[1].description == "Step 3"
    
    def test_remove_nonexistent_step(self):
        """Test removing a step that doesn't exist."""
        session = TestSession(
            tc_id="TC_006",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        session.add_step(TestStep(step_number=1))
        
        result = session.remove_step(5)
        
        assert result is False
        assert len(session.steps) == 1
    
    def test_reorder_steps(self):
        """Test reordering steps by index."""
        session = TestSession(
            tc_id="TC_007",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        session.add_step(TestStep(step_number=1, description="First"))
        session.add_step(TestStep(step_number=2, description="Second"))
        session.add_step(TestStep(step_number=3, description="Third"))
        
        # Move first step to last position
        session.reorder_steps(0, 2)
        
        assert session.steps[0].description == "Second"
        assert session.steps[1].description == "Third"
        assert session.steps[2].description == "First"
        # Check renumbering
        assert session.steps[0].step_number == 1
        assert session.steps[1].step_number == 2
        assert session.steps[2].step_number == 3
    
    def test_get_duration(self):
        """Test session duration calculation."""
        session = TestSession(
            tc_id="TC_008",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        duration = session.get_duration()
        
        # Should return formatted duration string
        assert isinstance(duration, str)
        assert ":" in duration
        # Format should be HH:MM:SS
        parts = duration.split(":")
        assert len(parts) == 3
    
    def test_get_overall_status_pass(self):
        """Test overall status when all steps pass."""
        session = TestSession(
            tc_id="TC_009",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        session.add_step(TestStep(step_number=1, result="Pass"))
        session.add_step(TestStep(step_number=2, result="Pass"))
        
        assert session.get_overall_status() == "PASS"
    
    def test_get_overall_status_fail(self):
        """Test overall status when any step fails."""
        session = TestSession(
            tc_id="TC_010",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        session.add_step(TestStep(step_number=1, result="Pass"))
        session.add_step(TestStep(step_number=2, result="Fail"))
        session.add_step(TestStep(step_number=3, result="Pass"))
        
        assert session.get_overall_status() == "FAIL"
    
    def test_get_overall_status_blocked(self):
        """Test overall status when steps are blocked."""
        session = TestSession(
            tc_id="TC_011",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        session.add_step(TestStep(step_number=1, result="Pass"))
        session.add_step(TestStep(step_number=2, result="Blocked"))
        
        assert session.get_overall_status() == "BLOCKED"
    
    def test_get_overall_status_no_steps(self):
        """Test overall status with no steps."""
        session = TestSession(
            tc_id="TC_012",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        assert session.get_overall_status() == "NO STEPS"
    
    def test_get_result_counts(self):
        """Test getting counts of each result type."""
        session = TestSession(
            tc_id="TC_013",
            tc_name="Test",
            module="Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        session.add_step(TestStep(step_number=1, result="Pass"))
        session.add_step(TestStep(step_number=2, result="Pass"))
        session.add_step(TestStep(step_number=3, result="Fail"))
        session.add_step(TestStep(step_number=4, result="Blocked"))
        session.add_step(TestStep(step_number=5, result="Untested"))
        
        counts = session.get_result_counts()
        
        assert counts["Pass"] == 2
        assert counts["Fail"] == 1
        assert counts["Blocked"] == 1
        assert counts["Untested"] == 1
    
    def test_session_to_dict(self):
        """Test TestSession serialization to dictionary."""
        session = TestSession(
            tc_id="TC_014",
            tc_name="Test Serialization",
            module="Core",
            environment="UAT",
            tester_name="Test User"
        )
        
        session.add_step(TestStep(step_number=1, description="Step 1"))
        
        session_dict = session.to_dict()
        
        assert isinstance(session_dict, dict)
        assert session_dict["tc_id"] == "TC_014"
        assert session_dict["tc_name"] == "Test Serialization"
        assert session_dict["module"] == "Core"
        assert session_dict["environment"] == "UAT"
        assert session_dict["tester_name"] == "Test User"
        assert len(session_dict["steps"]) == 1
        assert isinstance(session_dict["start_time"], str)
    
    def test_session_from_dict(self):
        """Test TestSession deserialization from dictionary."""
        data = {
            "session_id": "test1234",
            "tc_id": "TC_015",
            "tc_name": "Test Deserialization",
            "module": "Core",
            "environment": "PROD",
            "tester_name": "Test User",
            "start_time": "2026-08-19T10:00:00",
            "end_time": "2026-08-19T10:15:00",
            "steps": [
                {
                    "step_number": 1,
                    "timestamp": "2026-08-19 10:05:00",
                    "screenshot_path": "/test.png",
                    "annotated_path": "",
                    "highlight_rect": {},
                    "active_window": "Test",
                    "click_position": {},
                    "description": "Test step",
                    "result": "Pass"
                }
            ]
        }
        
        session = TestSession.from_dict(data)
        
        assert session.session_id == "test1234"
        assert session.tc_id == "TC_015"
        assert session.tc_name == "Test Deserialization"
        assert session.module == "Core"
        assert session.environment == "PROD"
        assert session.tester_name == "Test User"
        assert len(session.steps) == 1
        assert session.steps[0].description == "Test step"
    
    def test_session_roundtrip_serialization(self):
        """Test that session survives to_dict -> from_dict conversion."""
        original = TestSession(
            tc_id="TC_016",
            tc_name="Roundtrip Test",
            module="Test Module",
            environment="SIT",
            tester_name="Tester"
        )
        
        original.add_step(TestStep(step_number=1, description="Test"))
        
        session_dict = original.to_dict()
        restored = TestSession.from_dict(session_dict)
        
        assert restored.tc_id == original.tc_id
        assert restored.tc_name == original.tc_name
        assert restored.module == original.module
        assert restored.environment == original.environment
        assert restored.tester_name == original.tester_name
        assert len(restored.steps) == len(original.steps)
