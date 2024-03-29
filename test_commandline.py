import argparse

def init_argparser():
    parser = argparse.ArgumentParser(description= "Testing command line")

    parser.add_argument("dest_dir")
    parser.add_argument("-o", "--output")

    parser.parse_args()
    return parser

if __name__ == "__main__":
    init_argparser()