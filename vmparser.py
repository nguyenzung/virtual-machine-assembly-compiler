from distutils import command

from vmcommand import Command, CommandType


class Parser:

    arithmetic_ops = {"add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"}
    pop_ops = {"pop"}
    push_ops = {"push"}

    def __init__(self, path, input_file_name):
        self.file = open(path + input_file_name, "r")
        self.current_index = -1
        self.lines = self.file.readlines()
        return

    def has_more_command(self):
        return self.current_index < (len(self.lines) - 1)


    def parse_next(self):
        self.current_index += 1
        current_line = self.lines[self.current_index]
        current_line= current_line.replace("\n", "")
        current_line= current_line.replace("\t", "")
        lexicons = current_line.split(" ")
        command = Command()
        command.set_c_index(self.current_index)
        if lexicons[0] in Parser.arithmetic_ops:
            command.set_type(CommandType.C_ARITHMETIC)
            command.set_args(lexicons)
        elif lexicons[0] in Parser.pop_ops:
            command.set_type(CommandType.C_POP)
            command.set_args(lexicons[1:])
        elif lexicons[0] in Parser.push_ops:
            command.set_type(CommandType.C_PUSH)
            command.set_args(lexicons[1:])
        return command

    def finish(self):
        self.file.close()
        return