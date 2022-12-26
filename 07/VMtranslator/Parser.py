from io import TextIOWrapper

from CommandType import CommandType

class Parser:
    class VMCommand:
        """
        1行のVM命令を保持するクラス
        """
        def __init__(self) -> None:
            self.type: str = "" # 命令の種類
            self.arg1: str = "" # 命令の第1引数。ただし、addのような算術命令の場合は、"add"となる
            self.arg2: int = -1 # 命令の第2引数
        

        def clear(self) -> None:
            self.type: str = ""
            self.arg1: str = ""
            self.arg2: int = -1


    def __init__(self, path_to_file: str) -> None:
        """
        path_to_fileはVMに入力されたVMファイルまでのパス
        """
        self.__file: TextIOWrapper = open(file=path_to_file, mode="r") # VMに入力されたVMファイル
        self.__current_vm_command: Parser.VMCommand = Parser.VMCommand() # 現在、処理している一行のVM命令
        self.__current_line: str = "" # 現在、処理しているVMファイルの一行（コメントや前後の空白を取り除いた状態）
        self.__command_type: CommandType = CommandType() # 命令の種類
    

    def __del__(self):
        self.__file.close()


    def __remove_comment(self, line: str) -> str:
        """
        lineからコメントを除去する
        """
        comment_position: int = line.find("//")
        return line[:comment_position]


    def __remove_tab(self, line: str) -> str:
        """
        lineから前後の空白を除去する
        """
        return line.strip()

    
    def __remove_newline_char_at_end(self, line: str):
        """
        lineの末尾の改行文字を除去する
        """
        return line.rstrip("\n")


    def __determine_command_type(self) -> None:
        """
        現在処理中の行の命令の種類を特定する
        """
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


    def __analyze_arithmetic_command(self) -> None:
        """
        addのような算術命令を解析する
        """
        line = self.__current_line
        line = self.__remove_tab(line=line)
        self.__current_vm_command.arg1 = self.__remove_newline_char_at_end(line=line)

    def __analyze_2_args_command(self, command_name: str) -> None:
        """
        pushやpopのような2つの引数がある命令を解析する。command_nameは"push"のような命令の名前
        """
        chunk: str = ""
        for char in self.__current_line[len(command_name)+1:]:
            if char.isspace():
                if self.__current_vm_command.arg1 == "":
                    self.__current_vm_command.arg1 = chunk
                    chunk = ""
                elif chunk == "":
                    # 1つ以上の空白に対応
                    continue
                else:
                    break
            else:
                chunk = chunk + char
        self.__current_vm_command.arg2 = int(self.__remove_newline_char_at_end(line=chunk))


    def __analyze_command(self) -> None:
        """
        現在着目している一行を解析する
        """
        self.__determine_command_type()
        if self.__current_vm_command.type == self.__command_type.c_push:
            self.__analyze_2_args_command(command_name="push")
        elif self.__current_vm_command.type == self.__command_type.c_pop:
            self.__analyze_2_args_command(command_name="pop")
        else:
            self.__analyze_arithmetic_command()


    def hasMoreCommands(self) -> bool:
        """
        現在のVMファイル内で解析されていないVMファイルがあるか確認する。ある場合に限りTrueを返す
        """
        for line in self.__file:
            line = self.__remove_comment(line=line)

            if len(self.__remove_tab(line=line)) > 0:
                self.__current_line = line # 後のadvanceで使うので保持しておく
                return True
        return False


    def advance(self) -> None:
        """
        解析を一行分進める
        """
        self.__current_vm_command.clear()
        self.__analyze_command()


    def commandType(self) -> str:
        """
        解析し終えた命令の種類を返す
        """
        return self.__current_vm_command.type


    def arg1(self) -> str:
        """
        解析し終えた命令の第1引数を返す
        """
        return self.__current_vm_command.arg1


    def arg2(self) -> int:
        """
        解析し終えた命令の第2引数を返す
        """
        return self.__current_vm_command.arg2