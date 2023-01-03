import re
import sys
from io import TextIOWrapper

import Constant

class JackTokenizer:
    class Token:
        def __init__(self) -> None:
            self.type: int = Constant.NULL
            self.keyword: int = Constant.NULL
            self.symbol: str = ""
            self.identifier: str = ""
            self.int_val: int = -1
            self.string_val: str = ""
        

        def clear(self) -> None:
            self.type: int = Constant.NULL
            self.keyword: int = Constant.NULL
            self.symbol: str = ""
            self.identifier: str = ""
            self.int_val: int = -1
            self.string_val: str = ""

    
    class JackFileReader:
        """
        コメントを除去した形でJackファイルを1文字ずつ読み込むためのクラス
        """
        def __init__(self, path_to_jack_file: str) -> None:
            self.__codes: list[str] = []

            with open(file=path_to_jack_file, mode="r") as jack_file:
                COMMENT_PATTERN: str = "//.*$"
                code: str = ""

                while True:
                    code = jack_file.readline()
                    if code == "":
                        break

                    #code = re.sub(pattern=COMMENT_PATTERN, repl="", string=code) # コメントを除去
                    #code = code.strip() + "\n" # コード前後の空白を除去
                    self.__codes.append(code)
            
            self.__codes_index: int = 0
            self.__char_index: int = -1

        

        def get_char(self) -> str:
            return self.__codes[self.__codes_index][self.__char_index]
        

        def has_more_char(self) -> bool:
            if len(self.__codes[self.__codes_index]) > (self.__char_index + 1):
                return True
            elif len(self.__codes) > (self.__codes_index + 1):
                return True
            else:
                return False


        def advance(self) -> None:
            if len(self.__codes[self.__codes_index]) > (self.__char_index + 1):
                self.__char_index += 1
            elif len(self.__codes) > (self.__codes_index + 1):
                self.__codes_index += 1
                self.__char_index = 0
            else:
                JackTokenizer.JackFileReader.__error(message="内部エラー: JackTokenizer.JackFileReader.advance()が進み過ぎです\n")
        

        def retreat(self) -> None:
            if (self.__char_index - 1) > 0:
                self.__char_index -= 1
            elif (self.__codes_index - 1) > 0:
                self.__codes_index -= 1
                self.__char_index = len(self.__codes[self.__codes_index]) - 1
            else:
                JackTokenizer.JackFileReader.__error(message="内部エラー: JackTokenizer.JackFileReader.retreat()が後退し過ぎです")

        
        @staticmethod
        def __error(message: str) -> None:
            print(message)
            sys.exit(1)


    def __init__(self, path_to_input_file: str) -> None:
        self.__jack_file_reader: JackTokenizer.JackFileReader = JackTokenizer.JackFileReader(path_to_file=path_to_input_file)
        self.__token: JackTokenizer.Token = JackTokenizer.Token()
        # TODO: ハッシュを使うことで、余分な比較を少なくする 
        self.__KEYWORDS: list[str] = ["class",
                                    "constructor",
                                    "function",
                                    "method",
                                    "field",
                                    "static",
                                    "var",
                                    "int",
                                    "char",
                                    "boolean",
                                    "void",
                                    "true",
                                    "false",
                                    "null",
                                    "this",
                                    "let",
                                    "do",
                                    "if",
                                    "else",
                                    "while",
                                    "return"]
        self.__SYMBOLS: list[str] = ["{",
                                    "}",
                                    "(",
                                    ")",
                                    "[",
                                    "]",
                                    ".",
                                    ",",
                                    ";",
                                    "+",
                                    "-",
                                    "*",
                                    "/",
                                    "&",
                                    "|",
                                    "<",
                                    ">",
                                    "=",
                                    "~"]


    #
    # パブリックメソッド
    #

    def has_more_tokens(self) -> bool:
        while self.__jack_file_reader.has_more_char():
            self.__jack_file_reader.advance()
            char: str = self.__jack_file_reader.get_char()
            if char.isspace() or (char == "\n"):
                continue
            elif char == "/":
                self.__jack_file_reader.retreat()
            else:
                self.__jack_file_reader.retreat()
                return True
        return False


    def advance(self) -> None:
        chunk: str = self.__jack_file_reader.get_char()
        if chunk == "\"":
            self.__expect_string_constant()
        elif chunk.isdigit():
            self.__jack_file_reader.retreat()
            self.__expect_integer_constant()
        elif chunk == "/":
            self.__jack_file_reader.retreat()
            if not self.__expect_comment():
                self.__expect_symbol()
        elif not self.__expect_symbol():
            self.__jack_file_reader.retreat()
            self.__expect_keyword_or_identifer()



    def token_type(self) -> int:
        return self.__token.type


    def keyword(self) -> int:
        return self.__token.keyword


    def symbol(self) -> str:
        return self.__token.symbol


    def identifier(self) -> str:
        return self.__token.identifier


    def int_val(self) -> int:
        return self.__token.int_val


    def string_val(self) -> str:
        return self.__token.string_val


    #
    # プライベートメソッド
    #

    @staticmethod
    def __error(message: str) -> None:
        print(message)
        sys.exit(1)


    def __is_symbol(self, chunk: str) -> bool:
        for symbol in self.__SYMBOLS:
            if symbol == chunk:
                return  True
        return False
    

    def __set_keyword(self, keyword: str) -> None:
        self.__token.type = Constant.KEYWORD
        self.__token.keyword = keyword
    

    def __set_symbol(self, symbol: str) -> None:
        self.__token.type = Constant.SYMBOL
        self.__token.symbol = symbol
    

    def __set_integer_constant(self, int_const: int) -> None:
        self.__token.type = Constant.INT_CONST
        self.__token.int_val = int_const
    

    def __set_string_constant(self, str_constant: str) -> None:
        self.__token.type = Constant.STRING_CONST
        self.__token.string_val = str_constant
    

    def __set_identifier(self, identifier: str) -> None:
        self.__token.type = Constant.INDETIFIER
        self.__token.identifier = identifier
    

    def __expect_comment(self) -> bool:
        """
        コメントであれば、改行まで読み進める
        """
        char: str = ""

        for i in range(2):
            if not self.__jack_file_reader.has_more_char():
                for _ in range(i):
                    self.__jack_file_reader.retreat()
                    return False
            
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()

            if char != "/":
                for _ in range(i + 1):
                    self.__jack_file_reader.retreat()
                    return False
        
        # コメント以下の文字を消費
        while self.__jack_file_reader.has_more_char():
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()

            if char == "\n":
                return True


    def __expect_integer_constant(self) -> None:
        # 数字以外が出てくるまで、ファイルから読み込む
        chunk: str = ""
        char: str = ""

        while self.__jack_file_reader.has_more_char():
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()

            if char.isdigit():
                chunk += char
                continue
            else:
                self.__set_integer_constant(int_const=chunk)
                self.__jack_file_reader.retreat()
                return
    

    def __expect_string_constant(self) -> None:
        chunk: str = ""
        char: str = ""

        while self.__jack_file_reader.has_more_char():
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()

            if char == "\"":
                self.__set_string_constant(str_constant=chunk)
                return
            elif char == "\n":
                JackTokenizer.__error(message=f"{chunk}の後に\"がありません\n")
            else:
                chunk += char
    

    def __expect_symbol(self) -> bool:
        if self.__jack_file_reader.has_more_char():
            self.__jack_file_reader.advance()
            char: str = self.__jack_file_reader.get_char()
            if char in self.__SYMBOLS:
                self.__set_symbol(symbol=char)
                return True
            else:
                self.__jack_file_reader.retreat()
                return False
        else:
            JackTokenizer.__error(message="内部エラー: __expect_symbol()で処理する文字列がありません\n")
    

    def __expect_keyword_or_identifer(self) -> None:
        chunk: str = ""
        char: str = ""

        while self.__jack_file_reader.has_more_char():
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()

            if char == "\n":
                if self.__is_symbol(chunk=chunk):
                    self.__set_keyword(keyword=chunk)
                    return
                else:
                    self.__set_identifier(identifier=chunk)
                    return

            chunk += char
            if self.__is_symbol(chunk=chunk):
                self.__set_keyword(keyword=chunk)
                return
            else:
                self.__set_identifier(identifier=chunk)
                return
