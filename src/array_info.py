from typing import TypedDict

class DimInfo():
    lim_s: int
    R: int
    m: int

    def __init__(self) -> None:
        self.lim_s = 0
        self.R = 0
        self.m = 0
    
    def __init__(self, lim_s: int, R: int, m: int) -> None:
        self.lim_s = lim_s
        self.R = R
        self.m = m

class ArrayInfo:
    table: list()
    size: int

    def __init__(self) -> None:
        self.table = list()
        self.size = 0

    def add_dim(self, lim_s: int) -> DimInfo:
        """
        Insert the information of a new dimension corresponding to an array.

        Arguments:
        lim_s: int -- Superior limit defined for the dimension.
        """
        if lim_s > 0:
            curr_dim = len(self.table)
            if curr_dim == 0:
                self.table.append(DimInfo(lim_s, lim_s, 0))
            else:
                self.table.append(DimInfo(lim_s, self.table[curr_dim - 1].R  * lim_s, 0))
            return self.table[curr_dim]
        else:
            raise Exception("Arrays must have a dimension length larger than 0.")
    
    def update_dims(self) -> None:
        """
        Update the values of the m arguments of each node and array final size.
        """
        print(type(self.table))
        self.size = self.table[-1].R
        for i, dim in enumerate(self.table):
            if i == 0:
                self.table[i].m = self.size / dim.lim_s
            else:
                self.table[i].m =  self.table[i - 1].m / dim.lim_s