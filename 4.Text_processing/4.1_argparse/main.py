#!/bin/python3
import argparse
import sys


def main():
    parser = argparse.ArgumentParser(description="Convert yaml to json", prog="main",
                                     epilog="WAIT FOR YOUR MR")

    subparsers = parser.add_subparsers(title="My subparcers",
                                       help="My subparcers help")

    subparser_1 = subparsers.add_parser(name="yaml", help="yaml help")
    subparser_2 = subparsers.add_parser(name="json", help="json help")

    subparser_1.add_argument("-y", "--yaml_file", metavar="path/to/your/daemon.yaml",
                        help="path to yaml with docker daemon config", required=True)
    subparser_2.add_argument("-j", "--json_file")
    subparser_2.add_argument("-v", dest="is_validate", help="is need validation", nargs="+")

    args = parser.parse_args()

    print(args)


if __name__ == '__main__':
    main()

