from .utils.enums import Types, Operations
from typing import Dict


class SemanticCube:
    sem_cube: Dict[Types, Dict[Operations, Dict[Types, Types]]]

    def __init__(self):
        self.sem_cube = {
            Types.INT: {
                Operations.PLUS: {Types.INT: Types.INT, Types.FLOAT: Types.FLOAT},
                Operations.MINUS: {Types.INT: Types.INT, Types.FLOAT: Types.FLOAT},
                Operations.DIVIDES: {
                    Types.INT: Types.INT,
                    Types.FLOAT: Types.FLOAT,
                },
                Operations.TIMES: {Types.INT: Types.INT, Types.FLOAT: Types.FLOAT},
                Operations.GT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.EQGT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.LT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.EQLT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.EQ: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.DIFF: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.ASSIGNOP: {Types.INT: Types.INT, Types.FLOAT: Types.INT},
            },
            Types.FLOAT: {
                Operations.PLUS: {Types.INT: Types.FLOAT, Types.FLOAT: Types.FLOAT},
                Operations.MINUS: {Types.INT: Types.FLOAT, Types.FLOAT: Types.FLOAT},
                Operations.DIVIDES: {
                    Types.INT: Types.FLOAT,
                    Types.FLOAT: Types.FLOAT,
                },
                Operations.TIMES: {Types.INT: Types.FLOAT, Types.FLOAT: Types.FLOAT},
                Operations.GT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.EQGT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.LT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.EQLT: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.EQ: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.DIFF: {Types.INT: Types.BOOL, Types.FLOAT: Types.BOOL},
                Operations.ASSIGNOP: {
                    Types.INT: Types.FLOAT,
                    Types.FLOAT: Types.FLOAT,
                },
            },
            Types.STRING: {
                Operations.PLUS: {Types.STRING: Types.STRING},
                Operations.GT: {Types.STRING: Types.BOOL},
                Operations.EQGT: {Types.STRING: Types.BOOL},
                Operations.LT: {Types.STRING: Types.BOOL},
                Operations.EQLT: {Types.STRING: Types.BOOL},
                Operations.EQ: {Types.STRING: Types.BOOL},
                Operations.DIFF: {Types.STRING: Types.BOOL},
                Operations.ASSIGNOP: {Types.STRING: Types.STRING},
            },
            Types.BOOL: {
                Operations.EQ: {Types.BOOL: Types.BOOL},
                Operations.DIFF: {Types.BOOL: Types.STRING},
                Operations.ASSIGNOP: {Types.BOOL: Types.BOOL},
                Operations.OR: {Types.BOOL: Types.BOOL},
                Operations.AND: {Types.BOOL: Types.BOOL},
            },
        }

    def get(self, left_type: Types, oper: Operations, right_type: Types) -> Types:
        """
        Get the return type of an operation.

        Arguments:
        left_type: str -- Type of left operator.
        oper: str -- Operation requested.
        right_type: str -- Type of right operator.
        """
        try:
            result = self.sem_cube.get(left_type).get(oper).get(right_type)
        except Exception as e:
            raise TypeError("Type-mismatch of operands.") from None

        if result is None:
            raise TypeError("Type-mismatch of operands.")
        else:
            return result

    def has(self, left_type: Types, oper: Operations, right_type: Types) -> bool:
        """
        Check whether an operation is valid.

        Arguments:
        left_type: str -- Type of left operator.
        oper: str -- Operation requested.
        right_type: str -- Type of right operator.
        """
        return False if self.get(left_type, oper, right_type) is None else True