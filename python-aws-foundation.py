import argparse

from section_one import section_one


def main():
    if 1 in args.section:
        first_section = section_one.SectionOne()
        first_section.cis_check()


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-d",
        "--debug",
        help="output debug messages.",
        action="store_true"
    )
    parser.add_argument(
        "section",
        help="select which section to test.",
        nargs="+",
        type=int
    )
    args = parser.parse_args()
    main()
