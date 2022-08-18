import enum

from enum import Enum

class CommandType(Enum):
    C_PUSH=0,
    C_POP=1,
    C_ARITHMETIC=2,
    UNKNOWN=3


class Command:
    type = CommandType.UNKNOWN
    args = []
    c_index = 0

    def __init__(self):
        return

    def set_type(self, type):
        self.type = type
        return

    def get_type(self):
        return self.type

    def set_args(self, args):
        self.args = args
        return

    def get_args(self):
        return self.args

    def set_c_index(self, c_index):
        self.c_index = c_index
        return

    def get_c_index(self):
        return self.c_index

    def __str__(self) -> str:
        return "[{}]: {}".format(self.type, self.args)


if __name__ == "__main__":
    command = Command();
    print(command.get_type())
    print(command.get_args())
