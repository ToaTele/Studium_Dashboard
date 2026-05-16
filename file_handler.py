

class File_Handler:

    @staticmethod
    def to_file(_content):
        """gets a string and writes it to file"""
        #TODO Error
        with open("data.json", "w") as f:
            f.write(_content)

    @staticmethod
    def from_file():
        """reads a string from the file"""
        #TODO Error
        with open("data.json", "r") as f:
            _content = f.read()
        return _content