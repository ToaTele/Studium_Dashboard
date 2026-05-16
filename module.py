from datetime import datetime
from enum import Enum
from timer import Timer

class Module:
    name:str
    finished:bool = False
    grade:float = 0
    __timer:list[Timer] = []
    __exam:Enum

    def __init__(self, _name:str = '', _exam:Enum = None):
        self.name = _name
        self.__exam = _exam
        print("Module created: " + _name)

    def to_json(self):
        """Converts the Class to a JSON object"""
        _return = {'name': self.name, 'finished': self.finished, 'grade': self.grade, 'exam': self.__exam.value, 'timer': []}
        for _timer in self.__timer:
            _return['timer'].append(_timer.to_json())
        return _return

    def add_timer(self, _timer:Timer):
        """Adds a timer to the module"""
        if len(self.__timer) > 0:
            if self.__timer[-1].is_running:
                self.__timer[-1].stop()
        self.__timer.append(_timer)

    def start_timer(self):
        """Starts the active Timer"""
        self.__timer.append(Timer())
        self.__timer[-1].start()

    def stop_timer(self):
        """Stops the active Timer"""
        self.__timer[-1].stop()

    def get_time(self):
        """gets the whole time used for the module"""
        _time_used = 0
        for _timer in self.__timer:
            _time_used += _timer.saved_time
        return _time_used

    def __get_active_timer(self):
        return self.__timer[-1]

    active_timer = property(__get_active_timer)

class exam_type(Enum):
    exam = 1
    advanced_workbook = 2
    portfolio = 3