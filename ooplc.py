#
# @file LexerYaccOOPL.py
# @author David Luna and Yulisa Medina
# @brief
# @version 0.1
# @date 2022-03-07
#
# @copyright Copyright (c) 2022
#
#

# Libraries
import argparse
from pathlib import Path
from math import floor, ceil

# Internal modules
from src.lexer import Lexer
from src.parser import Parser
from src.utils.errors import OOPLError


def clamp(num: int, min_num: int, max_num: int) -> int:
    return max(min_num, min(num, max_num))


def printing_range(line_number: int, number_of_lines: int, context: int) -> range:
    min_num = clamp(line_number - floor(context / 2), 0, number_of_lines)
    max_num = clamp(line_number + ceil(context / 2), 0, number_of_lines)
    return range(min_num, max_num + 1)


def find_column(file_content: str, lexpos: int) -> int:
    line_start = file_content.rfind("\n", 0, lexpos) + 1
    return (lexpos - line_start) + 1


if __name__ == "__main__":
    argparser = argparse.ArgumentParser()
    argparser.add_argument("file", help="OOPL source file")
    argparser.add_argument(
        "-o", "--output", help="object file to generate", default="a.ooplobj"
    )
    argparser.add_argument(
        "-v",
        "--verbose",
        help="show additional information of the compilation process",
        action="store_true",
    )
    args = argparser.parse_args()
    # To execute lexer and parser, user will add the file to be tested as an argument

    # Build the lexer object
    lexer = Lexer()

    # Build the parser
    parser = Parser(lexer, args.verbose)
    try:
        with open(args.file, "r") as file:
            file_lines = file.readlines()
            file_content = "".join(file_lines).replace("\t", "    ")
            try:
                parser.parse(file_content)
            except OOPLError as e:
                col = find_column(file_content, e.char_pos)
                print(f"\nError in {file.name}")
                print(f"{Path(file.name).name}:{e.line_number}:{col}: {e.__str__()}\n")
                for line_no in printing_range(e.line_number, len(file_lines), 4):
                    line_to_print = file_lines[line_no - 1].removesuffix("\n")
                    print(f"\t{line_no}\t| {line_to_print}")
                    if line_no == e.line_number:
                        print(f"\t\t  {''.join([' '] * col)}^^^")
    except (EOFError, FileNotFoundError) as e:
        print(e)
