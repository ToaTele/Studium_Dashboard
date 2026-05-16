from course import course

class Student:
    firstname:str
    lastname:str
    __course:course

    def __init__(self, _firstname:str, _lastname:str, _course:course = None):
        #TODO Error
        self.firstname = _firstname
        self.lastname = _lastname
        print("new student created: " + self.firstname + " " + self.lastname)
        self.__course = _course

    def to_json(self):
        """Converts the Class to a JSON object"""
        #TODO Error
        _return = {'firstname': self.firstname, 'lastname': self.lastname, 'course': self.__course.to_json()}
        return _return

    def set_course(self, _course:course):
        """sets the course"""
        #TODO Error
        if self.__course is None:
            self.__course = _course
        else:
            raise Exception('There is already a course of study connected to this student.')
        pass

    def get_course(self) -> course:
        return self.__course

    course:course = property(get_course, set_course)