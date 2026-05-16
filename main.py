from time import sleep

from student import Student
from ui import ui
from threading import Thread
from file_data_handler import File_Data_Handler
_student:Student
_ui:ui

#TODO:
#   - Error
#   - Logging

if __name__ == '__main__':
    _ui = File_Data_Handler.load_data()
    if _ui is None:
        _student = Student("Max", "Mustermann")
        _ui = ui(_student)
    thread = Thread(target=_ui.init_ui)
    thread.start()
    pass