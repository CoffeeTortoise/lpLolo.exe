from sys import exit


class SaveLoad:
    @staticmethod
    def load(path):
        try:
            file = open(path, 'r')
            data = file.read()
            file.close()
            return data
        except FileNotFoundError:
            return 666

    @staticmethod
    def save(path, data):
        try:
            file = open(path, 'w')
            file.write(data)
            file.close()
        except FileNotFoundError:
            exit(1)
