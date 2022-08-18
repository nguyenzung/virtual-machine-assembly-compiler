from ast import arg
from vmcommand import Command, CommandType



class CodeWriter:

    def __init__(self, path, output_file_name):
        self.file_name = output_file_name
        self.file = open(path + output_file_name, "w")
        return

    def __write__(self, content):
        self.file.write(content + "\n")
        return

    def __increase_stack_pointer__(self):
        self.__write__("@SP")
        self.__write__("M=M+1")
        return

    def __decrease_stack_pointer__(self):
        self.__write__("@SP")
        self.__write__("M=M-1")
        return

    def __gen_code_for_push_constant__(self, index):
        self.__write__("@" + index)
        self.__write__("D=A")
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("M=D")
        self.__increase_stack_pointer__()
        return

    def __gen_code_for_push_lcl_arg_this_that__(self, segment, index):
        segment_mapper = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
        self.__write__("@" + index)
        self.__write__("D=A")
        self.__write__("@" + segment_mapper[segment])
        self.__write__("D=D+M")
        self.__write__("A=D")
        self.__write__("D=M")
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("M=D")
        self.__increase_stack_pointer__()
        return

    def __gen_code_for_push_static__(self, index):
        self.__write__("@" + self.file_name + "." + index)
        self.__write__("D=M")
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("M=D")
        self.__increase_stack_pointer__()
        return

    def __gen_code_for_push_temp__(self, index):
        self.__write__("@{}".format(5 + int(index)))
        self.__write__("D=M")
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("M=D")
        self.__increase_stack_pointer__()
        return

    def __gen_code_for_push_pointer__(self, index):
        segment_mapper = {"0": "THIS", "1": "THAT"}
        self.__write__("@" + segment_mapper[index])
        self.__write__("D=M")
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("M=D")
        self.__increase_stack_pointer__()
        return

    def __write_push_command__(self, command: Command):
        args = command.get_args()
        if args[0] == "constant":
            self.__gen_code_for_push_constant__(args[1])
        if args[0] in ["local", "argument", "this", "that"]:
            self.__gen_code_for_push_lcl_arg_this_that__(args[0], args[1])
        if args[0] == "static":
            self.__gen_code_for_push_static__(args[1])
        if args[0] == "pointer":
            self.__gen_code_for_push_pointer__(args[1])
        if args[0] == "temp":
            self.__gen_code_for_push_temp__(args[1])
        return

    def __gen_code_for_pop_static__(self, index):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("@" + self.file_name + "." + index)
        self.__write__("M=D")
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_pop_lcl_arg_this_that__(self, segment, index):
        segment_mapper = {"local": "LCL", "argument": "ARG", "this": "THIS", "that": "THAT"}
        self.__write__("@" + index)
        self.__write__("D=A")
        self.__write__("@" + segment_mapper[segment])
        self.__write__("M=D+M")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("@" + segment_mapper[segment])
        self.__write__("A=M")
        self.__write__("M=D")
        self.__write__("@" + index)
        self.__write__("D=A")
        self.__write__("@" + segment_mapper[segment])
        self.__write__("M=M-D")
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_pop_pointer__(self, index):
        segment_mapper = {"0": "THIS", "1": "THAT"}
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("@" + segment_mapper[index])
        self.__write__("M=D")
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_pop_temp__(self, index):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("@{}".format(5 + int(index)))
        self.__write__("M=D")
        self.__decrease_stack_pointer__()
        return

    def __write_pop_command__(self, command: Command):
        args = command.get_args()
        if args[0] == "pointer":
            self.__gen_code_for_pop_pointer__(args[1])
        if args[0] in ["local", "argument", "this", "that"]:
            self.__gen_code_for_pop_lcl_arg_this_that__(args[0], args[1])
        if args[0] == "static":
            self.__gen_code_for_pop_static__(args[1])
        if args[0] == "temp":
            self.__gen_code_for_pop_temp__(args[1])
        return

    def __gen_code_for_label_command__(self, label):
        self.__write__("({0})".format(label))
        return

    def __gen_code_for_goto_command__(self, label):
        self.__write__("@{0}".format(label))
        self.__write__("0;JMP")
        return

    def __gen_code_for_if_goto_command__(self, label):
        self.__decrease_stack_pointer__()
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("D=M")
        self.__write__("@{0}".format(label))
        self.__write__("D;JGT")
        return

    def __write_branching_command__(self, command: Command):
        args = command.get_args()
        if args[0] == "label":
            self.__gen_code_for_label_command__(args[1])
        if args[0] == "goto":
            self.__gen_code_for_goto_command__(args[1])
        if args[0] == "if-goto":
            self.__gen_code_for_if_goto_command__(args[1])
        return

    def __gen_code_for_and__(self):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("M=M&D")
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_or__(self):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("M=M|D")
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_not__(self):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("M=!M")
        return

    def __gen_code_for_add__(self):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("M=M+D")
        self.__decrease_stack_pointer__()
        return
    
    def __gen_code_for_sub__(self):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("M=M-D")
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_neg__(self):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("M=-M")
        return

    def __gen_code_for_eq__(self, c_index):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("D=M-D")
        self.__write__("@CHECK_TO_SET_EQ{}".format(c_index))
        self.__write__("0;JMP")
        self.__write__("(SET_LABEL_EQ{})".format(c_index))
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=-1")
        self.__write__("@FINISH_EQ{}".format(c_index))
        self.__write__("0;JMP")
        self.__write__("(CHECK_TO_SET_EQ{})".format(c_index))
        self.__write__("@SET_LABEL_EQ{}".format(c_index))
        self.__write__("D;JEQ")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=0")
        self.__write__("(FINISH_EQ{})".format(c_index))
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_gt__(self, c_index):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("D=M-D")
        self.__write__("@CHECK_TO_SET_GT{}".format(c_index))
        self.__write__("0;JMP")
        self.__write__("(SET_LABEL_GT{})".format(c_index))
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=-1")
        self.__write__("@FINISH_GT{}".format(c_index))
        self.__write__("0;JMP")
        self.__write__("(CHECK_TO_SET_GT{})".format(c_index))
        self.__write__("@SET_LABEL_GT{}".format(c_index))
        self.__write__("D;JGT")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=0")
        self.__write__("(FINISH_GT{})".format(c_index))
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_lt__(self, c_index):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("D=M-D")
        self.__write__("@CHECK_TO_SET_LT{}".format(c_index))
        self.__write__("0;JMP")
        self.__write__("(SET_LABEL_LT{})".format(c_index))
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=-1")
        self.__write__("@FINISH_LT{}".format(c_index))
        self.__write__("0;JMP")
        self.__write__("(CHECK_TO_SET_LT{})".format(c_index))
        self.__write__("@SET_LABEL_LT{}".format(c_index))
        self.__write__("D;JLT")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=0")
        self.__write__("(FINISH_LT{})".format(c_index))
        self.__decrease_stack_pointer__()
        return

    def __write_arithmetic_command__(self, command: Command):
        args = command.get_args()
        if args[0] == "add":
            self.__gen_code_for_add__()
        elif args[0] == "sub":
            self.__gen_code_for_sub__()
        elif args[0] == "neg":
            self.__gen_code_for_neg__()
        elif args[0] == "eq":
            self.__gen_code_for_eq__(command.get_c_index())
        elif args[0] == "gt":
            self.__gen_code_for_gt__(command.get_c_index())
        elif args[0] == "lt":
            self.__gen_code_for_lt__(command.get_c_index())
        elif args[0] == "and":
            self.__gen_code_for_and__()
        elif args[0] == "or":
            self.__gen_code_for_or__()
        elif args[0] == "not":
            self.__gen_code_for_not__()
        return

    def write_command(self, command: Command):
        print("Write command: " , command)
        type = command.get_type()
        if type == CommandType.C_ARITHMETIC:
            self.__write_arithmetic_command__(command)
        elif type == CommandType.C_PUSH:
            self.__write_push_command__(command)
        elif type == CommandType.C_POP:
            self.__write_pop_command__(command)
        elif type == CommandType.C_BRANCHING:
            self.__write_branching_command__(command)
        return

    def finish(self):
        self.file.close()
        return
