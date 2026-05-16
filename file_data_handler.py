import datetime
import json

import course
import module
import timer
from file_handler import File_Handler
import ui
import student


class File_Data_Handler:
    @staticmethod
    def save_data(_json: str):
        """gives data to file_handler"""
        File_Handler.to_file(_json)

    @staticmethod
    def load_data():
        """gets data from file_handler"""
        _file_content = File_Handler.from_file()
        _json_data = json.loads(_file_content)
        if _json_data["student"] is not None:
            _student = File_Data_Handler.student_from_json(_json_data["student"])
            _ui = ui.ui(_student)
            if _json_data["min_y"] is not None:
                _ui.min_y = int(_json_data["min_y"])
            if _json_data["max_y"] is not None:
                _ui.max_y = int(_json_data["max_y"])
            if _json_data["min_x"] is not None:
                _ui.min_x = int(_json_data["min_x"])
            if _json_data["max_x"] is not None:
                _ui.max_x = int(_json_data["max_x"])
            if _json_data["half_split"] is not None:
                _ui.half_split = int(_json_data["half_split"])
            if _json_data["daily_time"] is not None:
                _ui.daily_time = int(_json_data["daily_time"])
            return _ui
        return None

    @staticmethod
    def student_from_json(_json):
        """gets an object and turns it into a Student"""
        if _json["firstname"] is not None and _json["lastname"] is not None:
            _student = student.Student(_json["firstname"], _json["lastname"])
            if _json["course"] is not None:
                _student.course = File_Data_Handler.course_from_json(_json["course"])
            return _student
        return None

    @staticmethod
    def course_from_json(_json):
        """gets an object and turns it into a Course"""
        if _json["name"] is not None and _json["start_date"] is not None:
            _course = course.course(_json["name"], _start_date=datetime.datetime.strptime(_json["start_date"], '%Y-%m-%d %H:%M:%S'))
            if _json["modules"] is not None:
                for _module in _json["modules"]:
                    _course.add_module(File_Data_Handler.module_from_json(_module))
            if _json["amount_semester"] is not None:
                _course.amount_semester = _json["amount_semester"]
            if _json["active_module"] is not None:
                _course.active_module = _json["active_module"]
            return _course
        return None

    @staticmethod
    def module_from_json(_json):
        """gets an object and turns it into a Module with Timers"""
        if _json["name"] is not None and _json["exam"] is not None:
            _module = module.Module(_json["name"], module.exam_type(_json["exam"]))
            if _json["timer"] is not None:
                for _timer in _json["timer"]:
                    _module.add_timer(timer.Timer(_timer["saved_time"]))
            if _json["finished"] is not None:
                _module.finished = _json["finished"]
            if _json["grade"] is not None:
                _module.grade = _json["grade"]
            return _module
        return None
