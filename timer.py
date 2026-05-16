from datetime import datetime

class Timer:
    __start_time:datetime = None
    __stop_time:datetime = None
    saved_time:int = 0 # for better performance, I will save the used time in this variable
    def __init__(self, saved_time:int = 0):
        self.saved_time = saved_time

    def to_json(self):
        """Converts the Class to a JSON object"""
        return {'saved_time': self.saved_time}

    def start(self):
        """Starts the timer"""
        if self.__start_time is None:
            self.__start_time = datetime.now()
        else:
            raise "Timer has already been started: "

    def stop(self):
        """Stops the timer"""
        self.__stop_time = datetime.now()
        self.saved_time = self.__calculate_time()

    def __calculate_time(self):
        """Calculates the time it used"""
        return self.date_diff_in_seconds(self.__stop_time, self.__start_time)

    def date_diff_in_seconds(self, dt2, dt1):
        """Calculates the difference between two datetimes"""
        # Calculate the time difference between dt2 and dt1
        timedelta = dt2 - dt1
        # Return the total time difference in seconds
        return timedelta.days * 24 * 3600 + timedelta.seconds

    def __get_run_time(self):
        return self.date_diff_in_seconds(datetime.now(), self.__start_time)

    run_time = property(__get_run_time)

    def __get_is_running(self):
        return self.__start_time is not None and self.__stop_time is None

    is_running = property(__get_is_running)