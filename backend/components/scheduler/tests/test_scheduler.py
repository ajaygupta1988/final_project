import unittest, sys, os
from unittest.mock import patch, MagicMock
import time
path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.append(path)
from scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.execution_times = []

    def example_task(self):
        self.execution_times.append(time.time())

    @patch('scheduler.threading.Timer')
    def test_scheduler_start(self, MockTimer):
        # Mock Timer to control its behavior
        mock_timer_instance = MagicMock()
        MockTimer.return_value = mock_timer_instance

        scheduler = Scheduler(interval=1, task=self.example_task)
        start_time = time.time()
        scheduler.start()

        # The task should run immediately
        self.assertEqual(len(self.execution_times), 1)
        self.assertAlmostEqual(self.execution_times[0], start_time, delta=0.1)

        # Simulate timer triggering the task
        scheduler._run()

        self.assertEqual(len(self.execution_times), 2)

        # Stop the scheduler and ensure the timer is canceled
        scheduler.stop()
        mock_timer_instance.cancel.assert_called_once()

    @patch('scheduler.threading.Timer')
    def test_scheduler_stop(self, MockTimer):
        # Mock Timer to control its behavior
        mock_timer_instance = MagicMock()
        MockTimer.return_value = mock_timer_instance

        scheduler = Scheduler(interval=1, task=self.example_task)
        scheduler.start()

        # Simulate timer triggering the task twice
        scheduler._run()
        scheduler._run()

        self.assertEqual(len(self.execution_times), 3)  # Initial run + 2 runs

        scheduler.stop()

        # Ensure no further tasks are run after stopping
        scheduler._run()
        self.assertEqual(len(self.execution_times), 3)
        mock_timer_instance.cancel.assert_called_once()

if __name__ == "__main__":
    unittest.main()