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
        self.__write__("D=D+M")
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("M=D")
        self.__write__("A=A-1")
        self.__write__("D=M")
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("A=M")
        self.__write__("M=D")
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
        self.__write__("({0}{1})".format(self.file_name, label))
        return

    def __gen_code_for_goto_command__(self, label):
        self.__write__("@{0}{1}".format(self.file_name, label))
        self.__write__("0;JMP")
        return

    def __gen_code_for_if_goto_command__(self, label):
        self.__decrease_stack_pointer__()
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("D=M")
        self.__write__("@{0}{1}".format(self.file_name, label))
        self.__write__("D;JNE")
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
        self.__write__("M=0")
        self.__write__("@FINISH_EQ{}".format(c_index))
        self.__write__("D;JNE")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=-1")
        self.__write__("(FINISH_EQ{})".format(c_index))
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_gt__(self, c_index):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("D=M-D")
        self.__write__("M=0")
        self.__write__("@FINISH_EQ{}".format(c_index))
        self.__write__("D;JLE")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=-1")
        self.__write__("(FINISH_EQ{})".format(c_index))
        self.__decrease_stack_pointer__()
        return

    def __gen_code_for_lt__(self, c_index):
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("A=A-1")
        self.__write__("D=M-D")
        self.__write__("M=0")
        self.__write__("@FINISH_EQ{}".format(c_index))
        self.__write__("D;JGE")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("A=A-1")
        self.__write__("M=-1")
        self.__write__("(FINISH_EQ{})".format(c_index))
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

    def __gen_code_for_function_declare__(self, functionName, nVars):
        self.__write__("({0})".format(functionName))        
        self.__write__("@SP")
        self.__write__("A=M")
        for i in range(int(nVars)):
            self.__write__("M=0")
            self.__write__("A=A+1")
        # Index SP
        self.__write__("D=A")
        self.__write__("@SP")
        self.__write__("M=D")
        return

    def __gen_code_for_push_data_from_D__(self):
        self.__write__("@SP")
        self.__write__("A=M")
        self.__write__("M=D")
        self.__increase_stack_pointer__()
        return

    def __gen_code_for_function_call__(self, functionName, nArgs, c_index):
        # Save return address
        self.__write__("// Call function {}".format(functionName))
        self.__write__("@{0}.ret{1}".format(self.file_name, c_index))
        self.__write__("D=A")
        self.__gen_code_for_push_data_from_D__()
        
        # Save LCL
        self.__write__("// SAVE LCL")
        self.__write__("@LCL")
        self.__write__("D=M")
        self.__gen_code_for_push_data_from_D__()
        
        # Save ARG
        self.__write__("// SAVE ARG")
        self.__write__("@ARG")
        self.__write__("D=M")
        self.__gen_code_for_push_data_from_D__()
        
        # Save THIS
        self.__write__("// SAVE THIS")
        self.__write__("@THIS")
        self.__write__("D=M")
        self.__gen_code_for_push_data_from_D__()
        
        # Save THAT
        self.__write__("// Save THAT")
        self.__write__("@THAT")
        self.__write__("D=M")
        self.__gen_code_for_push_data_from_D__()

        # Index ARG
        self.__write__("// Index ARG")
        self.__write__("@SP")
        self.__write__("D=M")
        self.__write__("@{0}".format(int(nArgs) + 5))
        self.__write__("D=D-A")
        self.__write__("@ARG")
        self.__write__("M=D")

        # Index LCL
        self.__write__("// Index LCL")
        self.__write__("@SP")
        self.__write__("D=M")
        self.__write__("@LCL")
        self.__write__("M=D")

        # JUMP
        self.__write__("@{0}".format(functionName))
        self.__write__("0;JMP")

        # Return point
        self.__write__("({0}.ret{1})".format(self.file_name, c_index))
        return

    def __gen_code_for_return__(self):
        # Index endframe
        self.__write__("// Restore endframe")
        self.__write__("@LCL")
        self.__write__("D=M")
        self.__write__("@R13")
        self.__write__("M=D")

        # Return address
        self.__write__("@5")
        self.__write__("A=D-A")
        self.__write__("D=M")
        self.__write__("@R14")
        self.__write__("M=D")

        # Return value
        self.__write__("// Restore value")
        self.__write__("@SP")
        self.__write__("A=M-1")
        self.__write__("D=M")
        self.__write__("@ARG")
        self.__write__("A=M")
        self.__write__("M=D")

        # Restore SP
        self.__write__("// Restore sp")
        self.__write__("D=A+1")
        self.__write__("@SP")
        self.__write__("M=D")

        # Restore THAT
        self.__write__("// Restore that")
        self.__write__("@R13")
        self.__write__("M=M-1")
        self.__write__("A=M")
        self.__write__("D=M")
        self.__write__("@THAT")
        self.__write__("M=D")

        # Restore THIS
        self.__write__("// Restore this")
        self.__write__("@R13")
        self.__write__("M=M-1")
        self.__write__("A=M")
        self.__write__("D=M")
        self.__write__("@THIS")
        self.__write__("M=D")

        # Restore ARG
        self.__write__("// Restore arg")
        self.__write__("@R13")
        self.__write__("M=M-1")
        self.__write__("A=M")
        self.__write__("D=M")
        self.__write__("@ARG")
        self.__write__("M=D")

        # Restore LCL
        self.__write__("// Restore lcl")
        self.__write__("@R13")
        self.__write__("M=M-1")
        self.__write__("A=M")
        self.__write__("D=M")
        self.__write__("@LCL")
        self.__write__("M=D")

        # JUMP Back
        self.__write__("// JMP back")
        self.__write__("@R14")
        self.__write__("A=M")
        self.__write__("0;JMP")

        return

    def __write_function_command__(self, command: Command):
        args = command.get_args()
        if args[0] == "function":
            self.__gen_code_for_function_declare__(args[1], args[2])
        if args[0] == "call":
            self.__gen_code_for_function_call__(args[1], args[2], command.get_c_index())
        if args[0] == "return":
            self.__gen_code_for_return__()
        return

    def write_command(self, command: Command):
        type = command.get_type()
        if type == CommandType.C_ARITHMETIC:
            # self.__write__("// [CMD]: {}".format(command))
            self.__write_arithmetic_command__(command)
        elif type == CommandType.C_PUSH:
            # self.__write__("// [CMD]: {}".format(command))
            self.__write_push_command__(command)
        elif type == CommandType.C_POP:
            # self.__write__("// [CMD]: {}".format(command))
            self.__write_pop_command__(command)
        elif type == CommandType.C_BRANCHING:
            # self.__write__("// [CMD]: {}".format(command))
            self.__write_branching_command__(command)
        elif type == CommandType.C_FUNCTION:
            # self.__write__("// [CMD]: {}".format(command))
            self.__write_function_command__(command)
        return

    def finish(self):
        self.file.close()
        return
