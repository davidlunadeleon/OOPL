from re import T
from utils.enums import Types, Operations

class SemanticCube:
    sem_cube = dict()

    def __init__(self):
        self.sem_cube = {
            Types.INT: {
                "+": {
                    Types.INT: {
                        Types.INT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },
                "-": {
                    Types.INT: {
                        Types.INT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },
                "/": {
                    Types.INT: {
                        Types.INT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },
                "*": {
                    Types.INT: {
                        Types.INT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },

                ">": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                ">=": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "<": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "<=": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "==": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "!=": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "=": {
                    Types.INT: {
                        Types.INT
                    },
                    Types.FLOAT: {
                        Types.INT
                    }
                },  
            },

            Types.FLOAT: {
                "+": {
                    Types.INT: {
                        Types.FLOAT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },
                "-": {
                    Types.INT: {
                        Types.FLOAT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },
                "/": {
                    Types.INT: {
                        Types.FLOAT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },
                "*": {
                    Types.INT: {
                        Types.FLOAT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },

                ">": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                ">=": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "<": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "<=": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "==": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "!=": {
                    Types.INT: {
                        Types.BOOL
                    },
                    Types.FLOAT: {
                        Types.BOOL
                    }
                },
                "=": {
                    Types.INT: {
                        Types.FLOAT
                    },
                    Types.FLOAT: {
                        Types.FLOAT
                    }
                },  
            },

            Types.STRING: {
                "+": {
                    Types.STRING: {
                        Types.STRING
                    }
                },
                ">": {
                    Types.STRING: {
                        Types.BOOL
                    }
                },
                ">=": {
                    Types.STRING: {
                        Types.BOOL
                    }
                },
                "<": {
                    Types.STRING: {
                        Types.BOOL
                    }
                },
                "<=": {
                    Types.STRING: {
                        Types.BOOL
                    }
                },
                "==": {
                    Types.STRING: {
                        Types.BOOL
                    }
                },
                "!=": {
                    Types.STRING: {
                        Types.BOOL
                    }
                },
                "=": {
                    Types.STRING: {
                        Types.STRING
                    }
                }
            },
            
            Types.BOOL: {
                "==": {
                    Types.BOOL: {
                        Types.BOOL
                    }
                },
                "!=": {
                    Types.BOOL: {
                        Types.STRING
                    }
                },
                "=": {
                    Types.BOOL: {
                        Types.BOOL
                    }
                },
                "||": {
                    Types.BOOL: {
                        Types.BOOL
                    }
                },
                "&&": {
                    Types.BOOL: {
                        Types.BOOL
                    }
                }
            }
        }
    
    def getType(self, left_type: str, oper: str ,right_type: str) -> Types:
        """
        Get the return type of an operation.

        Arguments:
        left_type: str -- Type of left operator.
        oper: str -- Operation requested.
        right_type: str -- Type of right operator.
        """
        try:
            left_type = Types(left_type)
            # oper = Operations(oper)
            right_type = Types(right_type)
            return self.sem_cube.get(left_type).get(oper).get(right_type)
        except Exception as e:
            raise TypeError('Type-mismatch of operands.') from None
    
    def has(self, left_type: str, oper: str ,right_type: str) -> bool:
        """
        Check whether an operation is valid.

        Arguments:
        left_type: str -- Type of left operator.
        oper: str -- Operation requested.
        right_type: str -- Type of right operator.
        """
        left_type = Types(left_type)
        # oper = Operations(oper)
        right_type = Types(right_type)
        return False if self.getType(left_type, oper, right_type) is None else True

buffer = SemanticCube()
print(buffer.has('bool', '||', 'bool'))