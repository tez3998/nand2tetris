import re
import sys
from io import TextIOWrapper

import Constant

class Parser:
    class VmCommand:
        def __init__(self) -> None:
            self.type: int = -1
            self.arg1: str = ""
            self.arg2: str = ""
        

        def clear(self) -> None:
            self.type: int = -1
            self.arg1: str = ""
            self.arg2: str = ""


    #
    # パブリックメソッド
    #
    def __init__(self, path_to_input_file: str) -> None:
        self.__input_file: TextIOWrapper = open(file=path_to_input_file, mode="r")
        self.__current_vm_command: Parser.VmCommand = Parser.VmCommand()
        self.__current_line: str = ""


    def __del__(self) -> None:
        self.__input_file.close()


    def has_more_commands(self) -> bool:
        for line in self.__input_file:
            line = self.__remove_comment(line=line)
            line = self.__remove_space(line=line)
            line = self.__remove_newline_char_at_end(line=line)
            if len(line) == 0:
                return False
            else:
                self.__current_line = line
                return True


    def advance(self) -> None:
        self.__current_vm_command.clear()
        command_name: str = self.__determine_command_type()

        cmd_type: int = self.__current_vm_command.type
        if cmd_type == Constant.C_ARITHMETIC:
            # 本当は余計な文字列が続いていないかチェックする必要がある
            self.__current_vm_command.arg1 = command_name
        elif cmd_type == Constant.C_LABEL or cmd_type == Constant.C_GOTO or cmd_type == Constant.C_IF:
            self.__parse_1_args_command(command_name=command_name)
        else:
            self.__parse_2_args_command(command_name=command_name)


    def command_type(self) -> int:
        return self.__current_vm_command.type


    def arg1(self) -> str:
        return self.__current_vm_command.arg1


    def arg2(self) -> int:
        return self.__current_vm_command.arg2
    

    #
    # プライベートメソッド
    #
    def __remove_comment(self, line: str) -> str:
        COMMENT_PATTERN: str = "//.*$"
        return re.sub(pattern=COMMENT_PATTERN, repl="", string=line)
    

    def __remove_space(self, line: str) -> str:
        return line.strip()
    

    def __remove_newline_char_at_end(self, line: str) -> str:
        return line.rstrip("\n")
    

    def __determine_command_type(self) -> str:
        chunk: str = ""
        
        for char in self.__current_line:
            chunk += char
            if chunk == "push":
                self.__current_vm_command.type = Constant.C_PUSH
                return chunk

            elif chunk == "pop":
                self.__current_vm_command.type = Constant.C_POP
                return chunk

            elif chunk == "label":
                self.__current_vm_command.type = Constant.C_LABEL
                return chunk

            elif chunk == "goto":
                self.__current_vm_command.type = Constant.C_GOTO
                return chunk

            elif chunk == "if-goto":
                self.__current_vm_command.type = Constant.C_IF
                return chunk

            elif chunk == "function":
                self.__current_vm_command.type = Constant.C_FUNCTION
                return chunk

            elif chunk == "return":
                self.__current_vm_command.type = Constant.C_RETURN
                return chunk

            elif chunk == "call":
                self.__current_vm_command.type = Constant.C_CALL
                return chunk

            elif chunk == "add" or\
                 chunk == "sub" or\
                 chunk == "neg" or\
                 chunk == "eq" or\
                 chunk == "gt" or\
                 chunk == "lt" or\
                 chunk == "and" or\
                 chunk == "or" or\
                 chunk == "not":
                self.__current_vm_command.type = Constant.C_ARITHMETIC
                return chunk
        
        print(f"不明な命令です：{self.__current_line}\n")
        sys.exit(1)


    def __parse_1_args_command(self, command_name: str) -> None:
        chunk: str = ""
        for char in self.__current_line[len(command_name+1):]:
            if char.isspace():
                continue
            else:
                chunk += char
        # 本当は余計な文字列が続いていないかチェックする必要がある
        self.__current_vm_command.arg1 = chunk
        



    def __parse_2_args_command(self, command_name: str) -> None:
        chunk: str = ""
        for char in self.__current_line[len(command_name+1):]:
            if char.isspace():
                if self.__current_vm_command.arg1 == "":
                    self.__current_vm_command.arg1 = chunk
                    chunk = ""
                elif chunk == "": # 複数の空白に対応
                    continue
                else:
                    break
            else:
                chunk += char
        # 本当は余計な文字列が続いていないかチェックする必要がある
        self.__current_vm_command.arg2 = chunk