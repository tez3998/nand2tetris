from io import TextIOWrapper

from CommandType import CommandType

class Parser:
    class VMCommand:
        def __init__(self) -> None:
            self.type: str = ""
            self.arg1: str = ""
            self.arg2: int = -1
        

        def clear(self) -> None:
            self.type: str = ""
            self.arg1: str = ""
            self.arg2: int = -1


    def __init__(self, path_to_file: str) -> None:
        self.__file: TextIOWrapper = open(file=path_to_file, mode="r")
        self.__current_vm_command: Parser.VMCommand = Parser.VMCommand()
        self.__current_line: str = ""
        self.__command_type: CommandType = CommandType()


    def __remove_comment(self, line: str) -> str:
        comment_position: int = line.find("//")
        return line[:comment_position]


    def __remove_tab(self, line: str) -> str:
        return line.strip()


    def __determine_command_type(self) -> None:
        chunk: str = ""
        for char in self.__current_line:
            chunk = chunk + char
            if chunk == "push":
                self.__current_vm_command.type = self.__command_type.c_push
                return
            elif chunk == "pop":
                self.__current_vm_command.type = self.__command_type.c_pop
                return
        # 本当はちゃんと算術命令になっているか確認するかをここで確認する必要がある
        self.__current_vm_command.type = self.__command_type.c_arithmetic


    def __analyze_2_args_command(self, command_name: str) -> None:
        chunk: str = ""
        for char in self.__current_line[len(command_name)+1:]:
            if char.isspace():
                self.__current_vm_command.arg1 = chunk
                chunk = ""
            else:
                chunk = chunk + char
        self.__current_vm_command.arg2 = int(chunk.rstrip("\n"))


    def __analyze_command(self) -> None:
        self.__determine_command_type()
        if self.__current_vm_command.type == self.__command_type.c_push:
            self.__analyze_2_args_command(command_name="push")
        elif self.__current_vm_command.type == self.__command_type.c_pop:
            self.__analyze_2_args_command(command_name="pop")


    def hasMoreCommands(self) -> bool:
        for line in self.__file:
            line = self.__remove_comment(line=line)

            if len(self.__remove_tab(line=line)) > 0:
                self.__current_line = line # 後のadvanceで使うので保持しておく
                return True
        return False


    def advance(self) -> None:
        self.__current_vm_command.clear()
        self.__analyze_command()


    def commandType(self) -> str:
        return self.__current_vm_command.type


    def arg1(self) -> str:
        return self.__current_vm_command.arg1


    def arg2(self) -> int:
        return self.__current_vm_command.arg2