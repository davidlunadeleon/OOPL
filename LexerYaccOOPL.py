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
from ply import lex
from ply import yacc
import sys

# Internal modules
from src.lexer import Lexer
from src.parser import Parser


# Build the lexer object
lexer = Lexer()

# Build the parser
parser = Parser(lexer)

if __name__ == "__main__":
    # To execute lexer and parser, user will add the file to be tested as an argument
    if len(sys.argv) == 2:
        name = sys.argv[1]
        try:
            with open(name, "r") as file:
                file_content = file.read()
                # Parse an expression
                parser.parse(file_content)
        except (EOFError, FileNotFoundError) as e:
            print(e)
    else:
        print(
            "Error: Incorrect argument list. Only one filename should be added for testing besides the file that contains the lexer and parser."
        )
