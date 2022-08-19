from genericpath import isdir, isfile
import os, sys

from vmparser import Parser
from vmcodewriter import CodeWriter

def create_asm_file_name(file_name):
    parts = file_name.split(".");
    return "{}.asm".format(parts[0])

def parse_file_path(file_path):
    file_path = file_path.rstrip("/")
    parts = file_path.split("/")
    print(parts)
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


def link(rootFile, files):
    print("[LINKING]", rootFile, files)
    open(rootFile, 'w').close()
    rootFileData = open(rootFile, "a")
    for file in files :
        fin = open(file, "r")
        data = fin.read()
        rootFileData.write(data)
        rootFileData.write("\n")
        fin.close()
    rootFileData.close()
    return

def translateFolder(path, input_folder_name):
    print("[Translate folder] {0}:{1}".format(path, input_folder_name))
    if path[len(path)-1:] != "/":
                path = "{}/".format(path)
    compiledFiles = ["bootstrap.asm.template", "{}Sys.asm".format(path)]
    files = os.listdir(path)
    for file in files:
        if len(file) > 3 and file[len(file)-3:] == ".vm":            
            outFile = translateFile(path, file)
            if outFile != "Sys.asm":
                compiledFiles.append(path + outFile)
    link("{}{}.asm".format(path, input_folder_name), compiledFiles)
    return

def translateFile(path, input_file_name):
    print("[Translate file] {}".format(input_file_name))
    output_file_name = create_asm_file_name(input_file_name)
    print(input_file_name, output_file_name)
    translate(path, input_file_name, output_file_name)
    return output_file_name

def main():
    print("VM Translator")
    if len(sys.argv) != 2:
        print("Usage: python3 translator.py <file_name.vm>/<folder_name>")
        return
    path, input_file_name = parse_file_path(sys.argv[1])
    if os.path.isdir(sys.argv[1]):
        translateFolder(sys.argv[1], input_file_name)
    elif os.path.isfile(sys.argv[1]):
        translateFile(path, input_file_name)
    return

if __name__ == "__main__":
    main()