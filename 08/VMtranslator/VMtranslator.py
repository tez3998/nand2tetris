import os
import re
import sys

from CodeWriter import CodeWriter
import Constant
from Parser import Parser


def get_final_path(path: str) -> str:
    return os.path.basename(p=os.path.normpath(path=path))


def generete_output_file_name(path: str):
    final_path: str = get_final_path(path=path)
    if re.match(pattern=".vm$", string=final_path) != None:
        return re.sub(pattern=".vm$", repl=".asm", string=final_path)
    else:
        return final_path + ".asm"


def main():
    PATH_TO_FILE_OR_DIR: str = sys.argv[1]
    input_files : list[str] = []
    output_file_name = generete_output_file_name(path=PATH_TO_FILE_OR_DIR)
    START_FILE_NAME = "Sys.vm"

    # 各ファイルまでのパスをリスト化
    if os.path.isdir(s=PATH_TO_FILE_OR_DIR):
        path_to_dir: str = PATH_TO_FILE_OR_DIR
        for file_candidate_name in os.listdir(path=path_to_dir):
            path_to_file_candidate: str = os.path.join(path_to_dir, file_candidate_name)
            if os.path.isfile(path=path_to_file_candidate):
                if file_candidate_name == START_FILE_NAME:
                    input_files.insert(0, path_to_file_candidate)
                elif re.match(pattern=".*vm$", string=file_candidate_name) != None:
                    input_files.append(path_to_file_candidate)
    elif os.path.isfile(path=PATH_TO_FILE_OR_DIR):
        path_to_file: str = PATH_TO_FILE_OR_DIR
        input_files.append(path_to_file)
    else:
        print("引数に有効なファイルかディレクトリまでのパスを指定してください\n")
        sys.exit(1)

    # アセンブリの生成
    code_writer: CodeWriter = CodeWriter(output_file_name=output_file_name)

    code_writer.write_init()
    for input_file in input_files:
        parser: Parser = Parser(path_to_input_file=input_file)
        input_file_name: str = get_final_path(path=input_file)
        code_writer.set_file_name(file_name=re.sub(pattern=".vm$", repl="", string=input_file_name))

        while parser.has_more_commands():
            parser.advance()
            cmd_type: int = parser.command_type()

            if cmd_type == Constant.C_ARITHMETIC:
                cmd: str = parser.arg1()
                code_writer.write_arithmetic(command=cmd)
            elif cmd_type == Constant.C_PUSH:
                segment: str = parser.arg1()
                index: int = parser.arg2()
                code_writer.write_push_pop(command="push", segment=segment, index=index)
            elif cmd_type == Constant.C_POP:
                segment: str = parser.arg1()
                index: int = parser.arg2()
                code_writer.write_push_pop(command="pop", segment=segment, index=index)
            elif cmd_type == Constant.C_LABEL:
                label: str = parser.arg1()
                code_writer.write_label(label=label)
            elif cmd_type == Constant.C_GOTO:
                label: str = parser.arg1()
                code_writer.write_goto(label=label)
            elif cmd_type == Constant.C_IF:
                label: str = parser.arg1()
                code_writer.write_if(label=label)
            elif cmd_type == Constant.C_FUNCTION:
                function_name: str = parser.arg1()
                num_locals: int = parser.arg2()
                code_writer.write_function(function_name=function_name, num_locals=num_locals)
            elif cmd_type == Constant.C_RETURN:
                code_writer.write_return()
            elif cmd_type == Constant.C_CALL:
                function_name: str = parser.arg1()
                num_args: int = parser.arg2()
                code_writer.write_call(function_name=function_name, num_args=num_args)
            else:
                print("命令の種類が不正です\n")
                sys.exit(1)
        
    code_writer.close()


if __name__ == "__main__":
    main()
