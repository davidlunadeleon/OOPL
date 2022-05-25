import argparse

from src.vm import VM
from src.utils.enums import Segments, Operations

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="OOPL object file")
    parser.add_argument("-o", "--output", help="file to print the output to")
    args = parser.parse_args()

    segment = None
    segments = [s.value for s in Segments]
    vm = VM()

    try:
        with open(args.file, "r") as file:
            for line in file.readlines():
                line = line.removesuffix("\n")

                if line[0] == "#":
                    # Skip comments and debug information.
                    continue
                if line in segments:
                    segment = Segments(line)
                    continue
                else:
                    line = line.split(",")

                if segment is Segments.GLOBAL_MEMORY:
                    if line[1] != "None":
                        vm.set_global_variable(int(line[0]), line[1])
                elif segment is Segments.FUNCTIONS:
                    vm.add_function(
                        line[0],
                        int(line[1]),
                        (int(line[2]), int(line[3]), int(line[4]), int(line[5])),
                    )
                    pass
                elif segment is Segments.QUADRUPLES:
                    addr1 = None if line[1] == "None" else int(line[1])
                    addr2 = None if line[2] == "None" else int(line[2])
                    try:
                        addr3 = None if line[3] == "None" else int(line[3])
                    except ValueError:
                        addr3 = line[3]
                    vm.add_quadruple((Operations(line[0]), addr1, addr2, addr3))
                elif segment is Segments.GLOBAL_RESOURCES:
                    vm.init_global_memory(
                        (int(line[0]), int(line[1]), int(line[2]), int(line[3]))
                    )
        vm.run()
        vm.global_memory.print(True)
        vm.function_memory.print(True)
    except (EOFError, FileNotFoundError) as e:
        print(e)
