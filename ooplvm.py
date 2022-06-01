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
                elif line in segments:
                    segment = Segments(line)
                    continue

                match segment:
                    case Segments.GLOBAL_MEMORY:
                        index = line.find(",")
                        line = [line[:index], line[index + 1 :]]
                        line[1] = line[1].replace("\\n", "\n").replace("\\t", "\t")
                        if line[1] != "None":
                            vm.set_global_variable(int(line[0]), line[1])
                    case Segments.FUNCTIONS:
                        line = line.split(",")
                        vm.add_function(
                            line[0],
                            int(line[1]),
                            (
                                int(line[2]),
                                int(line[3]),
                                int(line[4]),
                                int(line[5]),
                                int(line[6]),
                            ),
                        )
                        pass
                    case Segments.QUADRUPLES:
                        line = line.split(",")
                        addr1 = int(line[1])
                        addr2 = int(line[2])
                        addr3 = int(line[3])
                        vm.add_quadruple((Operations(line[0]), addr1, addr2, addr3))
                    case Segments.GLOBAL_RESOURCES:
                        line = line.split(",")
                        vm.init_global_memory(
                            (
                                int(line[0]),
                                int(line[1]),
                                int(line[2]),
                                int(line[3]),
                                int(line[4]),
                            )
                        )
        vm.run()
    except (EOFError, FileNotFoundError) as e:
        print(e)
