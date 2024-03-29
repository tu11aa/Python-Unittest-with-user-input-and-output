import argparse

def init_argparser():
    parser = argparse.ArgumentParser(description= "Testing command line")

    parser.add_argument("dest_dir", default="exercises")
    parser.add_argument("-o", "--output", default="scoring table.json")

    parser.parse_args()
    return parser

if __name__ == "__main__":
    init_argparser()