import json
import math
import os
from math import ceil, floor
from time import sleep
from threading import Thread

import colorama
from colorama import Fore, Back, Style, Cursor
import msvcrt

import file_data_handler
from student import Student
from module import Module
from timer import Timer


class ui:
    min_y:int = 1
    max_y:int = 50
    min_x:int = 1
    max_x:int = 82
    half_split:int = 40
    daily_time:int = 7200 #saved time in File
    __time_spent:int = 0
    __student:Student
    __timer:Timer = None
    __module_output = []
    def __init__(self, student: Student):
        self.__student = student

    def to_json(self):
        """Converts the Class to a JSON object"""
        _return = {'min_y': self.min_y, 'max_y': self.max_y, 'min_x': self.min_x, 'max_x': self.max_x, 'half_split': self.half_split, 'daily_time': self.daily_time, 'student': self.__student.to_json()}
        return json.dumps(_return)

    def clear(self):
        """Clears the ui"""
        for y in range(self.min_y, 1 + self.max_y):
            for x in range(self.min_x, 1 + self.max_x):
                print(Cursor.POS(x, y), end='')
                print(' ', end='')
        print(Cursor.POS(self.min_y, self.min_x), end='')

    def init_ui(self):
        """initiate ui, print out the border and the first data"""
        if os.get_terminal_size().columns < self.max_x:
            #TODO Error
            pass
        if os.get_terminal_size().lines < self.max_y:
            #TODO Error
            pass
        colorama.just_fix_windows_console()
        self.clear()
        self.draw_border()
        self.update_headline()
        self.update_active_module()
        self.update_open_modules()
        self.update_grade_overview()
        self.update_course_overview()
        self.update_daily_overview()
        self.update_timer()
        self.update_footer()
        self.input_handler()

    def input_handler(self):
        """this function handles the user input"""
        while True:
            if msvcrt.kbhit():
                _input = msvcrt.getch()
                if _input == b'q':
                    #Quit
                    self.stop()
                    self.clear()
                    break
                elif _input == b'n':
                    #End course and input grade
                    if not self.__student.course.get_modules()[self.__student.course.active_module].finished:
                        self.handle_end_module()
                elif _input == b't':
                    #Toggle Timer
                    self.handle_toggle_timer_input()
                elif _input == b'1':
                    #change active course
                    self.change_active_module(0)
                elif _input == b'2':
                    #change active course
                    self.change_active_module(1)
                elif _input == b'3':
                    #change active course
                    self.change_active_module(2)
                elif _input == b'o':
                    #Save
                    file_data_handler.File_Data_Handler.save_data(self.to_json())
            print('') # ohne diese Zeile wird die UI nicht aktualisiert
            self.print_at_xy('', self.min_x, self.min_y) # damit der Cursor immer oben bleibt
            sleep(.1)

    def stop(self):
        """this function is called when the user stops the application with the appropriate key"""
        if self.__timer is not None and self.__timer.is_running:
            self.__timer.stop()

    def check_str_max_length(self, _str:str, _max_length:int, _fill:bool = True):
        """checks that the string is not too long for the ui, and fills the rest with blanks, so that old test will be cleared"""
        if len(_str) > _max_length:
            _str = _str[0:_max_length]
        if _fill:
            _str = _str.ljust(_max_length, ' ')
        return _str

    def update_headline(self):
        """Updates the headline"""
        _headline:str = 'Dashboard ' + self.__student.firstname + ' ' + self.__student.lastname
        _max_length = (self.max_x - (self.min_x + 3))
        _headline = self.check_str_max_length(_headline, _max_length, False)
        _start_x:int = floor((_max_length - len(_headline)) / 2)
        self.print_at_xy(_headline, self.min_x + _start_x, self.min_y + 1)

    def print_at_xy(self, _text:str, _x:int, _y:int):
        """prints the text at the x / y coordinates"""
        print(Cursor.POS(_x, _y), end='')
        print(_text, end='')
        print(Cursor.POS(self.min_x, self.min_y), end='')

    def update_active_module(self):
        """Updates the active module"""
        _line1:str = 'Aktiver Kurs: '
        _length:int = self.max_x - (self.min_x + 3)
        _line2:str = ''
        for i in range(_length):
            _line2 += '-'
        _active_module:Module = self.__student.course.get_modules()[self.__student.course.active_module]
        _line3:str = self.check_str_max_length('Name           : ' + _active_module.name, _length)
        _line4:str = self.check_str_max_length('Geplante Abgabe: ', _length) #TODO
        if not _active_module.finished:
            _line5:str = '[N]ote eintragen und Kurs beenden'
        else:
            _line5:str = 'Kurs abgeschlossen                                               '
        self.print_at_xy(_line1, self.min_x + 2, 4)
        self.print_at_xy(_line2, self.min_x + 2, 5)
        self.print_at_xy(_line3, self.min_x + 2, 6)
        self.print_at_xy(_line4, self.min_x + 2, 7)
        self.print_at_xy(_line5, self.min_x + 2, 8)

    def change_active_module(self, _index):
        """changes the active module to the one that got selected"""
        if self.__timer is not None and self.__timer.is_running:
            self.__timer.stop()
        self.__student.course.active_module = self.__module_output[_index]
        self.update_active_module()
        self.update_open_modules()

    def handle_end_module(self):
        """ask the user for the grade of the module and mark it as finished"""
        _input = ""
        while not self.is_float(_input):
            _line:str = '                                                                 '
            self.print_at_xy(_line, self.min_x + 2, 8)
            print(Cursor.POS(self.min_x + 2, 8), end='')
            _input = input('Bitte Note eingeben("." als Trennzeichen nutzen): ')
        _float = float(_input)
        if _float > 6 or _float <= 0:
            #Error
            pass
        self.__student.course.get_modules()[self.__student.course.active_module].finished = True
        self.__student.course.get_modules()[self.__student.course.active_module].grade = _float
        self.update_active_module()
        self.update_course_overview()

    def update_open_modules(self):
        """Updates the open modules overview"""
        _line1:str = 'Offene Kurse: '
        _length: int = self.max_x - (self.min_x + 3)
        _line2: str = ''
        for i in range(_length):
            _line2 += '-'
        _modules = self.__student.course.get_modules()
        self.print_at_xy(_line1, self.min_x + 2, 10)
        self.print_at_xy(_line2, self.min_x + 2, 11)
        _counter:int = 0
        _output_counter:int = 0
        self.__module_output = []
        for _module in _modules:
            if not _module.finished:
                if _counter != self.__student.course.active_module:
                    if _output_counter < 3:
                        _output_counter += 1
                        self.__module_output.append(_counter)
                        _ouput = self.check_str_max_length('[' + str(_output_counter) + '] ' + _module.name, _length)
                        self.print_at_xy(_ouput, self.min_x + 2, 11+_output_counter)
            _counter += 1

    def update_grade_overview(self):
        """Updates the grade overview"""
        _line1:str = 'Notenübersicht: '
        _length: int = self.half_split - (self.min_x + 2)
        _line2: str = ''
        for i in range(_length):
            _line2 += '-'
        _line3:str = 'Durschnitt: ' #TODO
        _line4:str = 'Beste Note: ' #TODO
        self.print_at_xy(_line1, self.min_x + 2, 16)
        self.print_at_xy(_line2, self.min_x + 2, 17)
        self.print_at_xy(_line3, self.min_x + 2, 18)
        self.print_at_xy(_line4, self.min_x + 2, 19)

    def update_course_overview(self):
        """Updates the course overview"""
        _line1:str = 'Studienübersicht: '
        _length:int = self.half_split - (self.min_x + 2)
        _line2:str = ''
        for i in range(_length):
            _line2 += '-'
        _line3:str = 'Ziel: ' + str(self.__student.course.amount_semester) + ' Semester'
        _count_finished:int = 0
        for _module in self.__student.course.get_modules():
            if _module.finished:
                _count_finished += 1
        _line4:str = 'Status: '
        _percent = _count_finished / len(self.__student.course.get_modules())
        if _percent < 0.1:
            _line4 += "[----------]"
        elif 0.1 >= _percent < 0.2:
            _line4 += "[#---------]"
        elif 0.2 >= _percent < 0.3:
            _line4 += "[##--------]"
        elif 0.3 >= _percent < 0.4:
            _line4 += "[###-------]"
        elif 0.4 >= _percent < 0.5:
            _line4 += "[#####------]"
        elif 0.5 >= _percent < 0.6:
            _line4 += "[######----]"
        elif 0.6 >= _percent < 0.7:
            _line4 += "[#######---]"
        elif 0.7 >= _percent < 0.8:
            _line4 += "[########--]"
        elif 0.8 >= _percent < 0.8:
            _line4 += "[#########-]"
        elif 0.9 >= _percent:
            _line4 += "[##########]"
        self.print_at_xy(_line1, self.half_split + 3, 16)
        self.print_at_xy(_line2, self.half_split + 3, 17)
        self.print_at_xy(_line3, self.half_split + 3, 18)
        self.print_at_xy(_line4, self.half_split + 3, 19)

    def update_daily_overview(self):
        """Updates the daily overview"""
        _line1:str = 'Sitzungsübersicht: '
        _length: int = self.half_split - (self.min_x + 2)
        _line2: str = ''
        for i in range(_length):
            _line2 += '-'
        _ziel_min = math.floor(self.daily_time / 60)
        _ziel_sec = math.floor(self.daily_time % 60)
        _line3: str = 'Ziel:    ' + f"{_ziel_min:02}" + ":" + f"{_ziel_sec:02}"
        _spent_min = math.floor(self.__time_spent / 60)
        _spent_sec = math.floor(self.__time_spent % 60)
        _line4: str = 'Erldigt: ' + f"{_spent_min:02}" + ":" + f"{_spent_sec:02}"
        _diff = self.daily_time - self.__time_spent
        _diff_min = math.floor(_diff / 60)
        _diff_sec = math.floor(_diff % 60)
        _line5: str = 'Offen:   ' + f"{_diff_min:02}" + ":" + f"{_diff_sec:02}"
        self.print_at_xy(_line1, self.min_x + 2, 22)
        self.print_at_xy(_line2, self.min_x + 2, 23)
        self.print_at_xy(_line3, self.min_x + 2, 24)
        self.print_at_xy(_line4, self.min_x + 2, 25)
        self.print_at_xy(_line5, self.min_x + 2, 26)

    def handle_toggle_timer_input(self):
        """Handles the Timer toggle"""
        if self.__timer is None or not self.__timer.is_running:
            self.__student.course.get_modules()[self.__student.course.active_module].start_timer()
            self.__timer = self.__student.course.get_modules()[self.__student.course.active_module].active_timer
            _thread = Thread(target=self.loop_update_timer)
            _thread.start()
        else:
            self.__student.course.get_modules()[self.__student.course.active_module].stop_timer()
            self.__time_spent += self.__timer.saved_time
            self.__timer = None
            self.update_daily_overview()
        self.update_timer()

    def loop_update_timer(self):
        """Loop while timer is running and update ui"""
        while self.__timer is not None and self.__timer.is_running:
            self.update_timer_time()
            sleep(0.5)

    def update_timer_time(self):
        """Updates the timer time"""
        if self.__timer is None:
            _time_str = ""
        else:
            _time = self.__timer.run_time
            _minutes = math.floor(_time / 60)
            _seconds = math.floor(_time % 60)
            _time_str = f"{_minutes:02}" + ":" + f"{_seconds:02}"
        _line: str = 'Zeit:   ' + _time_str
        self.print_at_xy(_line, self.half_split + 3, 24)

    def update_timer(self):
        """Updates the timer overview"""
        _line1: str = 'Timer: '
        _length: int = self.half_split - (self.min_x + 2)
        _line2: str = ''
        for i in range(_length):
            _line2 += '-'
        if self.__timer is None:
            _status = "gestoppt      "
        else:
            if self.__timer.is_running:
                _status = "läuft         "
            else:
                _status = "gestoppt      "
        _line4: str = 'Status: ' + _status
        _line5: str = '[t] Start / Stop'
        self.print_at_xy(_line1, self.half_split + 3, 22)
        self.print_at_xy(_line2, self.half_split + 3, 23)
        self.update_timer_time()
        self.print_at_xy(_line4, self.half_split + 3, 25)
        self.print_at_xy(_line5, self.half_split + 3, 26)

    def update_footer(self):
        """Updates the footer"""
        _line1: str = '[o] zum speichern    [q] zum beenden'
        _max_length = (self.max_x - (self.min_x + 3))
        _line1 = self.check_str_max_length(_line1, _max_length, False)
        _start_x: int = floor((_max_length - len(_line1)) / 2)
        self.print_at_xy(_line1, self.min_x + _start_x, 28)

    def draw_border(self):
        """Draws the border"""
        print(Cursor.POS(self.min_x, self.min_y), end='')
        print('┌', end='')
        for i in range(self.max_x - (self.min_x + 1)):
            print('─', end='')
        print('┐')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y+1), end='')
        print('│')
        print('├', end='')
        for i in range(self.max_x - (self.min_x + 1)):
            print('─', end='')
        print('┤')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 3), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 4), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 5), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 6), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 7), end='')
        print('│')
        print('├', end='')
        for i in range(self.max_x - (self.min_x + 1)):
            print('─', end='')
        print('┤')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 9), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 10), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 11), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 12), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 13), end='')
        print('│')
        print('├', end='')
        for i in range(self.max_x - (self.min_x + 1)):
            print('─', end='')
        print('┤')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 15), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 15), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 16), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 16), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 17), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 17), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 18), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 18), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 19), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 19), end='')
        print('│')
        print('├', end='')
        for i in range(self.max_x - (self.min_x + 1)):
            print('─', end='')
        print('┤')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 21), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 21), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 22), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 22), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 23), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 23), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 24), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 24), end='')
        print('│')
        print('│', end='')
        print(Cursor.POS(self.min_x + self.half_split, self.min_y + 25), end='')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 25), end='')
        print('│')
        print('├', end='')
        for i in range(self.max_x - (self.min_x + 1)):
            print('─', end='')
        print('┤')
        print('│', end='')
        print(Cursor.POS(self.max_x, self.min_y + 27), end='')
        print('│')
        print('└', end='')
        for i in range(self.max_x - (self.min_x + 1)):
            print('─', end='')
        print('┘')

    def is_float(self, _string):
        """checks if string is a float"""
        try:
            float(_string)
            return True
        except ValueError:
            return False