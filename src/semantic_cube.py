from typing import Any

from .utils.enums import Types, Operations


class SemanticCube:
    sem_cube: dict[Any, dict[Operations, dict[Any, Any]]]

    def __init__(self):
        """
        Creating semantic cube TRIE which will be used to check if operations between operands are valid.
        """
        self.sem_cube = {
            Types.INT.value: {
                Operations.PLUS: {
                    Types.INT.value: Types.INT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.MINUS: {
                    Types.INT.value: Types.INT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.DIVIDES: {
                    Types.INT.value: Types.INT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.TIMES: {
                    Types.INT.value: Types.INT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.GT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.EQGT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.LT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.EQLT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.EQ: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.DIFF: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.ASSIGNOP: {
                    Types.INT.value: Types.INT.value,
                    Types.FLOAT.value: Types.INT.value,
                },
            },
            Types.FLOAT.value: {
                Operations.PLUS: {
                    Types.INT.value: Types.FLOAT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.MINUS: {
                    Types.INT.value: Types.FLOAT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.DIVIDES: {
                    Types.INT.value: Types.FLOAT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.TIMES: {
                    Types.INT.value: Types.FLOAT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
                Operations.GT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.EQGT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.LT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.EQLT: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.EQ: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.DIFF: {
                    Types.INT.value: Types.BOOL.value,
                    Types.FLOAT.value: Types.BOOL.value,
                },
                Operations.ASSIGNOP: {
                    Types.INT.value: Types.FLOAT.value,
                    Types.FLOAT.value: Types.FLOAT.value,
                },
            },
            Types.STRING.value: {
                Operations.PLUS: {Types.STRING.value: Types.STRING.value},
                Operations.GT: {Types.STRING.value: Types.BOOL.value},
                Operations.EQGT: {Types.STRING.value: Types.BOOL.value},
                Operations.LT: {Types.STRING.value: Types.BOOL.value},
                Operations.EQLT: {Types.STRING.value: Types.BOOL.value},
                Operations.EQ: {Types.STRING.value: Types.BOOL.value},
                Operations.DIFF: {Types.STRING.value: Types.BOOL.value},
                Operations.ASSIGNOP: {Types.STRING.value: Types.STRING.value},
            },
            Types.BOOL.value: {
                Operations.EQ: {Types.BOOL.value: Types.BOOL.value},
                Operations.DIFF: {Types.BOOL.value: Types.STRING.value},
                Operations.ASSIGNOP: {Types.BOOL.value: Types.BOOL.value},
                Operations.OR: {Types.BOOL.value: Types.BOOL.value},
                Operations.AND: {Types.BOOL.value: Types.BOOL.value},
            },
        }

    def get(self, left_type: str, oper: Operations, right_type: str) -> str:
        """
        Get the return type of an operation.

        Arguments:
        left_type: str -- Type of left operator.
        oper: str -- Operation requested.
        right_type: str -- Type of right operator.
        """
        try:
            result = self.sem_cube[left_type][oper][right_type]
        except KeyError as e:
            raise TypeError("Type-mismatch of operands.") from None

        return result

    def has(self, left_type: str, oper: Operations, right_type: str) -> bool:
        """
        Check whether an operation is valid.

        Arguments:
        left_type: str -- Type of left operator.
        oper: str -- Operation requested.
        right_type: str -- Type of right operator.
        """
        return False if self.get(left_type, oper, right_type) is None else True
