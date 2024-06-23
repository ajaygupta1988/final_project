import threading


class Scheduler:
    def __init__(self, interval, task):
        """
        Initializes the Scheduler with a specific interval and task.
        
        :param interval: Time interval in seconds between task executions
        :param task: The task (function) to be executed
        """
        self.interval = interval
        self.task = task
        self._timer = None
        self._is_running = False
        self._lock = threading.Lock()

    def _run(self):
        """
        Runs the scheduled task and reschedules it.
        """
        with self._lock:
            if self._is_running:
                self.task()
                self._timer = threading.Timer(self.interval, self._run)
                self._timer.start()

    def start(self):
        """
        Starts the scheduler to run the task immediately and then at the given interval.
        """
        with self._lock:
            if not self._is_running:
                self._is_running = True
                self.task()  # Run the task immediately
                self._timer = threading.Timer(self.interval, self._run)
                self._timer.start()

    def stop(self):
        """
        Stops the scheduler from running the task.
        """
        print('stopping scheduler')
        with self._lock:
            self._is_running = False
            if self._timer:
                self._timer.cancel()
                self._timer = None