import argparse

from .src.vm import VM
from .src.utils.enums import Segments

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
                if line[0] == "#":
                    # Skip comments and debug information.
                    continue
                if line in segments:
                    segment = Segments(line)
                print(line)
                if segment is Segments.GLOBAL_MEMORY:
                    pass
                elif segment is Segments.FUNCTIONS:
                    pass
                elif segment is Segments.QUADRUPLES:
                    pass
        vm.run()
    except (EOFError, FileNotFoundError) as e:
        print(e)
