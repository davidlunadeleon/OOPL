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

# Internal modules
from src.lexer import Lexer
from src.parser import Parser


# Build the lexer object
lexer = Lexer()

# Build the parser
parser = Parser(lexer)

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
    try:
        with open(args.file, "r") as file:
            file_content = file.read()
            # Parse an expression
            parser.parse(file_content)
    except (EOFError, FileNotFoundError) as e:
        print(e)
