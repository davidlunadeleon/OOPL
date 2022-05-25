import argparse

from src.vm import VM
from src.utils.enums import Segments

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
                    pass
                elif segment is Segments.GLOBAL_RESOURCES:
                    vm.init_global_memory(
                        (int(line[0]), int(line[1]), int(line[2]), int(line[3]))
                    )
        vm.func_dir.print(True)
        vm.run()
    except (EOFError, FileNotFoundError) as e:
        print(e)
