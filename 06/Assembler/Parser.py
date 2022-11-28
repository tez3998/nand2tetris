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
        self.__asm_file: TextIOWrapper = open(file=path_to_asm_file, mode="r") # アセンブリのファイル
        self.__current_command: Parser.AsmCommand = Parser.AsmCommand() # 現在のコマンド
        self.__current_line: str = "" # コメントと空白が除去された後のアセンブリの1行
        self.__command_type: CommandType = CommandType()
    
    def __del__(self):
        self.__asm_file.close()

    def __remove_comment(self, line: str) -> str:
        comment_position: int = line.find("//")
        return line[:comment_position]
    
    def __remove_tab(self, line: str) -> str:
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

    def hasMoreCommands(self) -> bool:
        line: str = self.__asm_file.readline()
        line = self.__remove_comment(line=line)
        line = self.__remove_tab(line=line)

        if len(line) > 0:
            self.__current_line = line # 後のadvanceで使うので保持しておく
            return True
        else:
            return False

    def advance(self) -> None:
        self.__current_command.clear()
        self.__analyze_command()

    def commandType(self) -> str:
        return self.__current_command.type

    def symbol(self) -> str:
        return self.__current_command.symbol

    def dest(self) -> str:
        return self.__current_command.dest

    def comp(self) -> str:
        return self.__current_command.comp

    def jump(self) -> str:
        return self.__current_command.jump