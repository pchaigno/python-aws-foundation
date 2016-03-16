import argparse

from aws_services import cloudtrail
from aws_services import ec2
from aws_services import iam
from aws_services import s3

from section.one import section_one
from section.two import section_two
from section.four import section_four


def main():

    CT = cloudtrail.CloudTrailService()
    EC2 = ec2.EC2Service()
    IAM = iam.IAMService()
    S3 = s3.S3Service()

    if 1 in args.section:
        first_section = section_one.SectionOne(IAM)
        first_section.cis_check()
    if 2 in args.section:
        second_section = section_two.SectionTwo(CT, S3)
        second_section.cis_check()
    if 4 in args.section:
        fourth_section = section_four.SectionFour(EC2)
        fourth_section.cis_check()


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
