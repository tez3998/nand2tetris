class CodeWriter:
    def __init__(self, output_file_name: str) -> None:
        pass


    def set_file_name(self, file_name: str) -> None:
        pass


    def write_init(self) -> None:
        pass


    def write_arithmetic(self, command: str) -> None:
        pass


    def write_push_pop(self, command: int, segment: str, index: int) -> None:
        pass


    def write_label(self, label: str) -> None:
        pass


    def write_goto(self, label: str) -> None:
        pass


    def write_if(self, label: str) -> None:
        pass


    def write_return(self) -> None:
        pass


    def write_function(self, function_name: str, num_locals: str) -> None:
        pass


    def close(self) -> None:
        pass