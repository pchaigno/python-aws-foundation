import csv
import argparse

try:
    import boto3
except ImportError:
    print("This script require Boto3 to be installed and configured.")
    quit()

from datetime import datetime


iam_client = boto3.client("iam")


def logging(message):
    """Custom logging function."""
    if args.verbosity and message is not None:
        print(message)


def get_credential_report():
    try:
        cred_report = iam_client.get_credential_report()
    except:
        iam_client.generate_credential_report()
    cred_report = iam_client.get_credential_report()
    return cred_report


def section_1_1(data):
    message = {
        "section_name": "1.1 Avoid the use of the \"root\" account (Scored)",
        "scored": True,
        "passed": True,
        "output": "root account is not in use"
    }
    csv_reader = csv.reader(data.splitlines(), delimiter=',')
    for row in csv_reader:
        if "root_account" in row[0]:
            logging("{}, {}, {}, {}".format(row[0], row[4], row[10], row[15]))
            message["output"] = "root account is still in use."
            message["passed"] = False
            break
    print("{}, passed : {}".format(message["section_name"], message["passed"]))


def section_1_2(data):
    message = {
        "section_name": "1.2 Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console password (Scored)",
        "scored": True,
        "passed": True,
        "output": "MFA is enabled for IAM users that have console password"
    }
    csv_reader = csv.reader(data.splitlines(), delimiter=',')
    for row in csv_reader:
        if "false" in row[7]:
            logging("{}, {}, {}".format(row[0], row[3], row[7]))
            message["output"] = "MFA is not enabled for all users"
            message["passed"] = False
            break
    print("{}, passed : {}".format(message["section_name"], message["passed"]))


def section_1_3(data):
    message = {
        "section_name": "1.3 Ensure credentials unused for 90 days or greater are disabled (Scored)",
        "scored": True,
        "passed": True,
        "output": "Old passwords are disabled"
    }
    csv_reader = csv.reader(data.splitlines(), delimiter=',')
    for row in csv_reader:
        if "true" in row[3]:
            date_ = datetime.strptime(row[4].split("T")[0], "%Y-%m-%d")
            now = datetime.now()
            delta = now - date_
            if delta.days > 90:
                message["output"] = "Old password is still enabled"
                message["passed"] = False
                break
    print("{}, passed : {}".format(message["section_name"], message["passed"]))


def section_1_4(data):
    message = {
        "section_name": "1.4 Ensure access keys are rotated every 90 days or less (Scored)",
        "scored": True,
        "passed": True,
        "output": "Access keys are rotated"
    }
    csv_reader = csv.reader(data.splitlines(), delimiter=',')
    for row in csv_reader:
        if "true" in row[8]:
            date_ = datetime.strptime(row[9].split("T")[0], "%Y-%m-%d")
            now = datetime.now()
            delta = now - date_
            if delta.days > 90:
                message["output"] = "Old access keys are still enabled"
                message["passed"] = False
            break
        if "true" in row[13]:
            date_ = datetime.strptime(row[14].split("T")[0], "%Y-%m-%d")
            now = datetime.now()
            delta = now - date_
            if delta.days > 90:
                message["output"] = "Old access keys are still enabled"
                message["passed"] = False
            break
    print("{}, passed : {}".format(message["section_name"], message["passed"]))


def main():
    """Main method of AWS-CIS Benchmark."""
    report_output = get_credential_report()

    section_1_1(report_output["Content"])
    section_1_2(report_output["Content"])
    section_1_3(report_output["Content"])
    section_1_4(report_output["Content"])


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-v",
        "--verbosity",
        help="increase output verbosity.",
        action="store_true"
    )
    args = parser.parse_args()
    main()
