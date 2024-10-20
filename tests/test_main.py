import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

# Create the FastAPI TestClient
TEST_URL = f"http://localhost:8000"
client = TestClient(app)

class TestFastAPIEndpoints(unittest.TestCase):

    def test_read_root(self):
        """Test the root endpoint."""
        response = client.get("/") 
        self.assertEqual(response.status_code, 200)
        self.assertIn("Inference Service", response.text)

    def test_health_check(self):
        """Test the health check endpoint."""
        with patch("app.main.redis_conn.ping", return_value=True):
            response = client.get("/health_check")
            self.assertIn(response.status_code, [200, 404])

    def test_send_text(self):
        """Test sending text to the inference service."""
        payload = {"text": "Hello", "with_medusa": True, "dyn_batch": True}
        response = client.post("/send_text", json=payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn("task_id", response.json())

    def test_get_task_status(self):
        """Test retrieving the task status."""
        with patch("app.main.AsyncResult") as mock_result:
            mock_result.return_value = MagicMock(state="SUCCESS", result="Task completed")
            response = client.get("/get_task_status/some-task-id")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "finished", "result": "Task completed"})

    def test_generate(self):
        """Test generating text with options."""
        payload = {"text": "Hello", "with_medusa": True, "dyn_batch": False}

        with patch("app.main.do_infer.apply_async") as mock_task:
            mock_task_instance = mock_task.return_value
            mock_task_instance.get.return_value = "Generated text"
            mock_task_instance.state = "SUCCESS"

            response = client.post("/generate", json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {"status": "finished", "result": "Generated text"}
            )


if __name__ == "__main__":
    unittest.main()
