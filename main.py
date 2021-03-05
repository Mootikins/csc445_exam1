import argparse
import graphviz


def make_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        usage="%(prog)s [options] file",
        description="Convert an NFA to a DFA, minimize a DFA, or both in sequence",
    )
    parser.add_argument("-c", "--nfa-to-dfa", help="convert an NFA to a DFA")
    parser.add_argument("-m", "--min-dfa", help="minimize a DFA")
    parser.add_argument("file")
    return parser


def main():
    parser = make_parser()
    args = parser.parse_args()
    try:
        gv = graphviz.Source.from_file(args.file)
        print(gv)
    except FileNotFoundError:
        print(f"Could not find file {args.file}")


if __name__ == "__main__":
    main()
