import os
import re
import sys
from io import TextIOWrapper

import Constant

class JackTokenizer:
    class Token:
        def __init__(self) -> None:
            self.type: str = ""
            self.keyword: str = ""
            self.symbol: str = ""
            self.identifier: str = ""
            self.int_val: int = -1
            self.string_val: str = ""
        

        def clear(self) -> None:
            self.type: str = ""
            self.keyword: str = ""
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
            self.__line_index: int = 0
            self.__char_index: int = -1

            with open(file=path_to_jack_file, mode="r") as jack_file:
                for line in jack_file:
                    self.__codes.append(line)
            
        
        def get_char(self) -> str:
            if self.__char_index == -1:
                self.__error(message=f"内部エラー: ファイル外にアクセスしています")
            else:
                return self.__codes[self.__line_index][self.__char_index]
        

        def get_current_position(self) -> str:
            return f"{self.__line_index+1}行{self.__char_index+1}字目"
                
        
        def get_line_index(self) -> int:
            return self.__line_index
        

        def get__char_index(self) -> int:
            return self.__char_index


        def has_more_char(self) -> bool:
            if (self.__char_index + 1) < len(self.__codes[self.__line_index]) or (self.__line_index + 1) < len(self.__codes):
                return True
            else:
                return False


        def advance(self) -> None:
            if (self.__char_index + 1) < len(self.__codes[self.__line_index]):
                self.__char_index += 1
                return
            elif (self.__line_index + 1) < len(self.__codes):
                self.__line_index += 1
                self.__char_index = 0
                return
            else:
                self.__error(message=f"内部エラー: JackFileReaderが進み過ぎです")


        def retreat(self) -> None:
            if self.__line_index == 0:
                if (self.__char_index - 1) >= -1:
                    self.__char_index -= 1
                    return
            
            if (self.__char_index - 1) >= 0:
                self.__char_index -= 1
                return
            elif (self.__line_index - 1) >= 0:
                self.__line_index -= 1
                self.__char_index = len(self.__codes[self.__line_index]) - 1
                return
            else:
                self.__error(message=f"内部エラー: JackFileReaderが戻り過ぎです")
            
        
        def __error(self, message: str):
            print(f"\n{message}; {self.get_current_position()};")
            print(f"{self.get_current_position()}: {message}")
            sys.exit(1)

    

    class XmlFileWriter:
        def __init__(self, path_to_file: str) -> None:
            self.__file: TextIOWrapper = open(file=path_to_file, mode="w")
            self.__write_start_tag()

        def __del__(self) -> None:
            self.__write_end_tag()
            self.__file.close()
        

        def write_tag(self, element_name: str, value: str) -> None:
            self.__file.write(f"<{element_name}> {value} </{element_name}>\n")
        

        def __write_start_tag(self) -> None:
            self.__file.write("<tokens>\n")
        

        def __write_end_tag(self) -> None:
            self.__file.write("</tokens>\n")


    def __init__(self, path_to_input_file: str, log: bool = False) -> None:
        self.__jack_file_name: str = os.path.basename(p=path_to_input_file) # エラー出力用に保持
        self.__log_flag: bool = log
        self.__jack_file_reader: JackTokenizer.JackFileReader = JackTokenizer.JackFileReader(path_to_jack_file=path_to_input_file)
        self.__token: JackTokenizer.Token = JackTokenizer.Token()
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
        path_to_output_file: str = re.sub(pattern="\.jack$", repl="T-generated.xml", string=path_to_input_file)
        self.__xml_file_writer: JackTokenizer.XmlFileWriter = JackTokenizer.XmlFileWriter(path_to_file=path_to_output_file)

    #
    # パブリックメソッド
    #

    def has_more_tokens(self) -> bool:
        # コメントはここで消費されるので、advanceには行かないはず
        char: str = ""

        while True:
            if not self.__jack_file_reader.has_more_char():
                self.__log("未処理のトークンなし")
                return False
            
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()

            if char == "/":
                if self.__expect_comment():
                    pass
                else:
                    self.__log(f"文字\"{char}\"からトークナイズを開始")
                    return True
            elif not (char == "\n" or char.isspace()):
                self.__log(f"文字\"{char}\"からトークナイズを開始")
                return True
            else:
                self.__log("改行またはスペースを検出")



    def advance(self) -> None:
        # ファイルに出力
        self.__token.clear()

        char: str = self.__jack_file_reader.get_char()

        if char.isdigit():
            self.__expect_integer_constant()
        elif char == "\"":
            self.__expect_string_constant()
        elif not self.__expect_symbol():
            if not self.__expect_keyword():
                self.__tokenize_identifier()

        self.__write_xml()


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
    def __error(self, message: str) -> None:
        message = message.replace("\n", "\\n")
        print(f"{self.__jack_file_name}:{self.__jack_file_reader.get_current_position()}: {message}")
        sys.exit(1)
    

    def __log(self, message: str) -> None:
        if not self.__log_flag:
            return
        message = message.replace("\n", "\\n")
        print(f"{self.__jack_file_name}:{self.__jack_file_reader.get_current_position()}: {message}")


    def __write_xml(self) -> None:
        token_type: str = self.token_type()

        if token_type == Constant.KEYWORD:
            self.__xml_file_writer.write_tag(element_name=token_type, value=self.keyword())
            return
        elif token_type == Constant.SYMBOL:
            self.__xml_file_writer.write_tag(element_name=token_type, value=self.symbol())
            return
        elif token_type == Constant.INDETIFIER:
            self.__xml_file_writer.write_tag(element_name=token_type, value=self.identifier())
            return
        elif token_type == Constant.INT_CONST:
            self.__xml_file_writer.write_tag(element_name=token_type, value=self.int_val())
            return
        elif token_type == Constant.STRING_CONST:
            self.__xml_file_writer.write_tag(element_name=token_type, value=self.string_val())
            return
        else:
            self.__error(message=f"内部エラー: トークンの種類が不正です: {token_type}\n")


    def __is_symbol(self, chunk: str) -> bool:
        return (chunk in self.__SYMBOLS)
    

    def __is_keyword(self, chunk: str) -> bool:
        return (chunk in self.__KEYWORDS)


    def __set_keyword(self, keyword: str) -> None:
        self.__log(f"keyword\"{keyword}\"を検出")

        self.__token.type = Constant.KEYWORD
        self.__token.keyword = keyword
    

    def __set_symbol(self, symbol: str) -> None:
        self.__log(f"symbol\"{symbol}\"を検出")

        self.__token.type = Constant.SYMBOL
        if symbol == ">":
            self.__token.symbol = "&gt;"
            return
        elif symbol == "<":
            self.__token.symbol = "&lt;"
            return
        elif symbol == "&":
            self.__token.symbol = "&amp;"
            return
        else:
            self.__token.symbol = symbol
            return
    

    def __set_integer_constant(self, int_const: int) -> None:
        self.__log(f"integerConstant\"{int_const}\"を検出")

        self.__token.type = Constant.INT_CONST
        self.__token.int_val = int_const
    

    def __set_string_constant(self, str_constant: str) -> None:
        self.__log(f"- stringConstant\"{str_constant}\"を検出")

        self.__token.type = Constant.STRING_CONST
        self.__token.string_val = str_constant
    

    def __set_identifier(self, identifier: str) -> None:
        self.__log(f"indentifier\"{identifier}\"を検出")

        self.__token.type = Constant.INDETIFIER
        self.__token.identifier = identifier
    

    def __expect_comment(self) -> bool:
        final_symbol: str = "" # 終端を示す記号
        chunk: str = self.__jack_file_reader.get_char()
        
        # コメントの種類の特定
        if not self.__jack_file_reader.has_more_char():
            return False
        self.__jack_file_reader.advance()
        chunk += self.__jack_file_reader.get_char()
        if chunk == "//":
            final_symbol = "\n"
            self.__log("一行のコメントを検出")
        elif chunk == "/*":
            final_symbol = "*/"
            self.__log("複数の行コメントを検出")
        else:
            self.__log(f"コメントを未検出")
            self.__jack_file_reader.retreat()
            return False
        
        # コメント分、readerを読み進める
        previous_char: str = ""
        current_char: str = ""

        if not self.__jack_file_reader.has_more_char():
            self.__error(message="コメントの終端記号がありません(1)")
        self.__jack_file_reader.advance()
        current_char = self.__jack_file_reader.get_char()

        if current_char == final_symbol:
            self.__log(f"コメントの分だけ読み進め完了")
            return True

        while True:
            if not self.__jack_file_reader.has_more_char():
                self.__error(message="コメントの終端記号がありません(2)")

            self.__jack_file_reader.advance()
            current_char = self.__jack_file_reader.get_char()
            
            if (previous_char + current_char) == final_symbol or current_char == final_symbol:
                self.__log(f"コメントの分だけ読み進め完了")
                return True
            
            previous_char = current_char
                



    def __expect_integer_constant(self) -> None:
        # 数字以外が出てくるまで、ファイルから読み込む
        chunk: str = ""
        char: str = self.__jack_file_reader.get_char()

        while True:
            if not char.isdigit():
                if chunk == "":
                    self.__error(message="内部エラー: __expect_integer_constant()のchunkが空です")
                
                self.__set_integer_constant(int_const=int(chunk))
                self.__jack_file_reader.retreat()
                return
            
            chunk += char
            if not self.__jack_file_reader.has_more_char():
                self.__error(message="内部エラー: __expect_integer_constant()の処理が途中で停止しました")
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()
    

    def __expect_string_constant(self) -> None:
        chunk: str = ""
        char: str = self.__jack_file_reader.get_char()
        FINAL_SYMBOL: str = "\""

        if char != "\"":
            self.__error(message="内部エラー: 文字列でないのに__expect_string_constant()が呼び出されました")
        
        while True:
            if not self.__jack_file_reader.has_more_char():
                self.__error(message="文字列の終端記号なしにコードが終了しました")
            
            self.__jack_file_reader.advance()
            char = self.__jack_file_reader.get_char()

            if char == "\n":
                self.__error(message="文字列の終端記号なしに改行文字が出現しました")
            elif char == FINAL_SYMBOL:
                self.__set_string_constant(str_constant=chunk)
                return
            else:
                chunk += char
    

    def __expect_symbol(self) -> bool:
        char: str = self.__jack_file_reader.get_char()
        if self.__is_symbol(chunk=char):
            self.__set_symbol(symbol=char)
            return True
        else:
            return False
    

    def __expect_keyword(self) -> bool:
        chunk: str = ""
        char: str = ""
        advanced_times: int = 0

        while True:
            char = self.__jack_file_reader.get_char()

            if char == "\n" or char.isspace():
                if self.__is_keyword(chunk=chunk):
                    self.__set_keyword(keyword=chunk)
                    self.__jack_file_reader.retreat()
                    return True
                else:
                    for _ in range(advanced_times):
                        self.__jack_file_reader.retreat()
                    return False
            elif self.__is_symbol(chunk=char):
                for _ in range(advanced_times):
                    self.__jack_file_reader.retreat()
                return False
            
            chunk += char

            if self.__is_keyword(chunk=chunk):
                self.__set_keyword(keyword=chunk)
                return True
            else:
                if not self.__jack_file_reader.has_more_char():
                    for _ in range(advanced_times):
                        self.__jack_file_reader.retreat()
                    return False
                else:
                    self.__jack_file_reader.advance()
                    advanced_times += 1
                    char = self.__jack_file_reader.get_char()



    def __tokenize_identifier(self) -> None:
        # 改行、空白、シンボル、まで読み込む
        chunk: str = ""
        char: str = self.__jack_file_reader.get_char()
        
        while True:
            if char == "\n" or char.isspace() or self.__is_symbol(chunk=char):
                if chunk == "":
                    self.__error(message="内部エラー: identifierが空です")
                else:
                    self.__set_identifier(identifier=chunk)
                    self.__jack_file_reader.retreat()
                    return
            else:
                chunk += char
                if not self.__jack_file_reader.has_more_char():
                    self.__error(f"identifierの途中でコードが終了しました")
                self.__jack_file_reader.advance()
                char = self.__jack_file_reader.get_char()