import datetime
from module import Module


class course:
    name:str
    start_date:datetime.date
    amount_semester:int = 0
    __modules: list[Module] = []
    __active_module:int = 0

    def __init__(self, _name:str, _start_date:datetime.datetime = datetime.datetime.now()):
        #TODO Error
        self.name = _name
        self.start_date = _start_date

    def to_json(self):
        """Converts the Class to a JSON object"""
        _return = {'name': self.name, 'start_date': datetime.datetime.strftime(self.start_date, '%Y-%m-%d %H:%M:%S'), 'amount_semester': self.amount_semester, 'active_module': self.active_module, 'modules': []}
        for _module in self.__modules:
            _return['modules'].append(_module.to_json())
        return _return

    def add_module(self, _module: Module):
        """Add a module to the course"""
        #TODO Error
        self.__modules.append(_module)

    def remove_module(self, _index: int):
        """Remove a module from the course by index"""
        #TODO Error
        del self.__modules[_index]

    def get_modules(self):
        """returns all modules in a list"""
        return self.__modules

    def set_active_module(self, _index: int):
        #TODO Error
        self.__active_module = _index

    def get_active_module(self):
        #TODO Error
        return self.__active_module

    active_module = property(get_active_module,set_active_module)