import glob
import os
import pathlib
import re
import sys

from JackTokenizer import JackTokenizer

class JackAnalyzer:
    def __init__(self, path_to_dir_or_file: str) -> None:
        self.__jack_files: list[str] = []

        if os.path.isfile(path=path_to_dir_or_file):
            self.__jack_files.append(path_to_dir_or_file)
        else:
            self.__jack_files = glob.glob(pathname=str(os.path.join(path_to_dir_or_file, "*.jack")))

    def tokenize(self) -> None:
        for file in self.__jack_files:
            tokenizer: JackTokenizer = JackTokenizer(path_to_input_file=file, log=True)
            while tokenizer.has_more_tokens():
                tokenizer.advance()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("用法: python JackAnalyzer.py [ディレクトリまたは.jackファイルまでのパス]\n")
        sys.exit(1)
    
    analyzer: JackAnalyzer = JackAnalyzer(path_to_dir_or_file=str(pathlib.Path(sys.argv[1]).resolve()))
    analyzer.tokenize()