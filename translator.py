import sys

from vmparser import Parser
from vmcodewriter import CodeWriter

def create_asm_file_name(file_name):
    parts = file_name.split(".");
    return "{}.asm".format(parts[0])

def parse_file_path(file_path):
    parts = file_path.split("/")
    file_name = parts[len(parts) - 1]
    path = "/".join(parts[0:len(parts) - 1])
    if path == "":
        path = "./"
    else:
        path += "/"
    return path, file_name

def translate(path, input_file_name, output_file_name):
    print("[TRANSLATE]", path, input_file_name, output_file_name)
    parser = Parser(path, input_file_name)
    code_writer = CodeWriter(path, output_file_name)
    while parser.has_more_command():
        command = parser.parse_next()
        code_writer.write_command(command)
    parser.finish()
    code_writer.finish()
    return

def main():
    print("VM Translator")
    if len(sys.argv) != 2:
        print("Usage: python3 translator.py <file_name.vm>")
        return
    path, input_file_name = parse_file_path(sys.argv[1])
    output_file_name = create_asm_file_name(input_file_name)
    translate(path, input_file_name, output_file_name)
    return

if __name__ == "__main__":
    main()