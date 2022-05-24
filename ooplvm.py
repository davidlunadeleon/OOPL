import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("file", help="OOPL object file")
    parser.add_argument("-o", "--output", help="file to print the output to")
    args = parser.parse_args()

    try:
        with open(args.file, "r") as file:
            pass
    except (EOFError, FileNotFoundError) as e:
        print(e)
