import unittest
import time
from scheduler import Scheduler

class TestScheduler(unittest.TestCase):
    def setUp(self):
        self.execution_times = []
        self.interval = 1

    def example_task(self):
        self.execution_times.append(time.time())

    def test_scheduler_start(self):
        scheduler = Scheduler(interval=self.interval, task=self.example_task)
        start_time = time.time()
        scheduler.start()

        # Allow the scheduler to run for a few intervals
        time.sleep(3.5)  # Wait for a bit more than 3 intervals

        scheduler.stop()

        # Check that the task ran immediately and then at the given intervals
        self.assertGreaterEqual(len(self.execution_times), 4)
        self.assertLessEqual(len(self.execution_times), 5)

        # Check that the first task execution was immediate
        self.assertAlmostEqual(self.execution_times[0], start_time, delta=0.1)

    def test_scheduler_stop(self):
        scheduler = Scheduler(interval=self.interval, task=self.example_task)
        scheduler.start()

        # Allow the scheduler to run for a couple of intervals
        time.sleep(2.5)  # Wait for a bit more than 2 intervals

        scheduler.stop()

        # Capture the length after stopping the scheduler
        length_after_stop = len(self.execution_times)

        # Wait for another couple of intervals to ensure no more tasks are executed
        time.sleep(2.5)

        self.assertEqual(len(self.execution_times), length_after_stop)

if __name__ == "__main__":
    unittest.main()