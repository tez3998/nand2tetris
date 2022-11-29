from io import TextIOWrapper

from CommandType import CommandType

class Parser:
    class AsmCommand:
        def __init__(self) -> None:
            self.type: str = ""
            self.symbol: str = ""
            self.dest: str = "null"
            self.comp: str = ""
            self.jump: str = "null"
        
        def clear(self) -> None:
            self.type: str = ""
            self.symbol: str = ""
            self.dest: str = "null"
            self.comp: str = ""
            self.jump: str = "null"

    def __init__(self, path_to_asm_file: str) -> None:
        """
        path_to_asm_fileはパースする.asmファイルまでのパス。
        """
        self.__asm_file: TextIOWrapper = open(file=path_to_asm_file, mode="r") # アセンブリのファイル
        self.__current_command: Parser.AsmCommand = Parser.AsmCommand() # 現在のコマンド
        self.__current_line: str = "" # コメントと空白が除去された後のアセンブリの1行
        self.__command_type: CommandType = CommandType()
    
    def __del__(self):
        self.__asm_file.close()

    def __remove_comment(self, line: str) -> str:
        """
        lineは.asmファイルの1行。
        1行からコメントを除去した結果を返す。
        """
        comment_position: int = line.find("//")
        return line[:comment_position]
    
    def __remove_tab(self, line: str) -> str:
        """
        lineは.asmファイルの1行。
        1行から空白を除去した結果を返す。
        """
        return line.strip()
    
    def __determine_command_type(self) -> None:
        char: str = self.__current_line[0]
        if char == "@":
            self.__current_command.type = self.__command_type.a
        elif char == "(":
            self.__current_command.type = self.__command_type.l
        else:
            self.__current_command.type = self.__command_type.c
    
    def __analyze_a_command(self) -> None:
        symbol: str = self.__current_line[1:]
        self.__current_command.symbol = symbol
    
    def __analyze_l_command(self) -> None:
        symbol: str = ""
        for char in self.__current_line[1:]:
            if char == ")":
                self.__current_command.symbol = symbol
                break # 本当はここでブレークせずに")"の後に余計な文字が入っていないかのチェックが必要
            else:
                symbol = symbol + char
    
    def __analyze_c_commamd(self) -> None:
        mnemonic: str = ""
        for char in self.__current_line:
            # 本当はdest, comp, jumpの順序を考える必要がある。
            if char == "=":
                self.__current_command.dest = mnemonic
                mnemonic = ""
            elif char == ";":
                self.__current_command.comp = mnemonic
                mnemonic = ""
            else:
                mnemonic = mnemonic + char
        if self.__current_command.comp == "":
            self.__current_command.comp = mnemonic
        else:
            self.__current_command.jump = mnemonic


    def __analyze_command(self) -> None:
        self.__determine_command_type()
        if self.__current_command.type == self.__command_type.a:
            self.__analyze_a_command()
        elif self.__current_command.type == self.__command_type.l:
            self.__analyze_l_command()
        else:
            self.__analyze_c_commamd()

    def returnToBeginning(self) -> None:
        self.__asm_file.seek(0)

    def hasMoreCommands(self) -> bool:
        for line in self.__asm_file:
            line = self.__remove_comment(line=line)
            line = self.__remove_tab(line=line)

            if len(line) > 0:
                self.__current_line = line # 後のadvanceで使うので保持しておく
                return True
        return False

    def advance(self) -> None:
        self.__current_command.clear()
        self.__analyze_command()

    def commandType(self) -> str:
        """
        命令の種類を返す。
        """
        return self.__current_command.type

    def symbol(self) -> str:
        """
        A命令またはL命令の場合に、シンボルを返す。
        """
        return self.__current_command.symbol

    def dest(self) -> str:
        """
        C命令の場合に、destを返す。
        """
        return self.__current_command.dest

    def comp(self) -> str:
        """
        C命令の場合に、compを返す。
        """
        return self.__current_command.comp

    def jump(self) -> str:
        """
        C命令の場合に、jumpを返す。
        """
        return self.__current_command.jump