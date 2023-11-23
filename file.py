import os, fileinput


class File:
    def __init__(self, path: str):
        self.path = path

    def write(self, input_: str):
        with open(self.path, 'w') as f:
            print(self.read())
            f.write(input_)
            print(self.read())
        f.close()

    def read(self):
        output = ''
        with open(self.path, 'r') as f:
            for line in f:
                output += line
        f.close()
        return output

    def __del__(self):
        pass
