import unittest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

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
            with patch("app.main.do_infer.apply_async") as mock_task:
                mock_task_instance = mock_task.return_value
                mock_task_instance.get.return_value = "Model healthy"
                mock_task_instance.state = "SUCCESS"

                response = client.get("/health_check")
                self.assertEqual(response.status_code, 200)
                self.assertIn("Model healthy", response.text)

    def test_send_text(self):
        """Test sending text to the inference service."""
        payload = {
            "text": "Hello", 
            "model_name": "vicuna_q2", 
            "dyn_batch": 2, 
            "speculative_decoding": True
        }
        with patch("app.main.do_infer.apply_async") as mock_task:
            mock_task.return_value.id = "test-task-id"

            response = client.post("/send_text", json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertIn("task_id", response.json())
            self.assertEqual(response.json()["task_id"], "test-task-id")

    def test_get_task_status(self):
        """Test retrieving the task status."""
        with patch("app.main.AsyncResult") as mock_result:
            mock_result.return_value = MagicMock(state="SUCCESS", result="Task completed")
            
            response = client.get("/get_task_status/some-task-id")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"status": "SUCCESS", "result": "Task completed"})

    def test_generate(self):
        """Test generating text with options."""
        payload = {
            "text": "Hello", 
            "model_name": "vicuna_q2", 
            "dyn_batch": 1, 
            "speculative_decoding": True
        }

        with patch("app.main.do_infer.apply_async") as mock_task:
            mock_task_instance = mock_task.return_value
            mock_task_instance.get.return_value = "Generated text"
            mock_task_instance.state = "SUCCESS"

            response = client.post("/generate", json=payload)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(
                response.json(),
                {"status": "SUCCESS", "result": "Generated text"}
            )

    def test_list_tasks(self):
        """Test listing all tasks."""
        with patch("app.main.redis_conn.keys", return_value=[b"task1", b"task2"]):
            response = client.get("/tasks/")
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {"tasks": ["task1", "task2"]})


if __name__ == "__main__":
    unittest.main()
