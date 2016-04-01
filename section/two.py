# -*- coding : utf8 -*-

from json import loads
from datetime import datetime, timedelta


class SectionTwo:

    def __init__(self, CT, S3):
        self.CT = CT
        self.S3 = S3

    def section_2_1(self):
        self.name = "2.1 Ensure CloudTrail is enabled in all regions"
        self.scored = True
        self.passed = False
        if self.CT.trailsReport:
            # check in every trail if IsMultiRegionTrail key is true
            for trail in self.CT.trailsReport:
                if trail["IsMultiRegionTrail"] is True:
                    self.S3.CTBucketName = trail["S3BucketName"]
                    self.passed = True
                    break
        print("{}, passed : {}".format(self.name, self.passed))

    def section_2_2(self):
        self.name = "2.2 Ensure CloudTrail log file validation is enabled"
        self.scored = True
        self.passed = True
        if self.CT.trailsReport:
            # for every trail, the LogFileValidationEnabled must be true
            for trail in self.CT.trailsReport:
                if trail["LogFileValidationEnabled"] is not True:
                    self.passed = False
                    break
        print("{}, passed : {}".format(self.name, self.passed))

    def section_2_3(self):
        self.name = "2.3 Ensure the S3 bucket CloudTrail logs to is not publicly accessible"
        self.scored = True
        self.passed = True
        if self.S3.CTBucketName is not None:
            S3BucketACL = self.S3.getS3BucketAcl(self.S3.CTBucketName)
            for grantee in S3BucketACL["Grants"]:
                if grantee["Grantee"]["Type"] == "Group":
                    if ("AuthenticatedUsers" or "AllUsers") in grantee["Grantee"]["URI"]:
                        self.passed = False
                        break
            S3BucketPolicy = self.S3.getS3BucketPolicy(self.S3.CTBucketName)
            # temporary fix, waiting for
            # https://github.com/aws/aws-cli/issues/1851
            S3BucketPolicy = loads(S3BucketPolicy["Policy"])
            for statement in S3BucketPolicy["Statement"]:
                if (
                    statement["Effect"] == "Allow" and
                    statement["Principal"] == "*"
                ):
                    self.passed = False
                    break
        else:
            # there is no S3 bucket used to store cloudtrail logs, so it can
            # not be publicly accessible, but we consider this test as failed
            self.passed = False
        print("{}, passed : {}".format(self.name, self.passed))

    def section_2_4(self):
        self.name = "2.4 Ensure CloudTrail trails are integrated with CloudWatch Logs"
        self.scored = True
        self.passed = False
        if self.CT.trailsReport:
            for trail in self.CT.trailsReport:
                if 'CloudWatchLogsLogGroupArn' in trail:
                    trailStatus = self.CT.getTrailStatus(trail["Name"])
                    date = trailStatus["LatestCloudWatchLogsDeliveryTime"].replace(tzinfo=None)
                    if date > datetime.now() - timedelta(days=1):
                        self.passed = True
        print("{}, passed : {}".format(self.name, self.passed))

    def section_2_5(self):
        self.name = "2.5 Ensure AWS Config is enabled in all regions"
        self.scored = True
        self.passed = False
        # This test requires the VM to be in US-East-1 (Virginia)
        # It will be implemented later

    def section_2_6(self):
        self.name = "2.6 Ensure S3 bucket access logging is enabled on the CloudTrail S3 bucket"
        self.scored = True
        self.passed = False
        if self.S3.CTBucketName is not None:
            logging_details = self.S3.getS3BucketLogging(self.S3.CTBucketName)
            if 'LoggingEnabled' in logging_details:
                self.passed = True
        print("{}, passed : {}".format(self.name, self.passed))

    def cis_check(self):
        self.section_2_1()
        self.section_2_2()
        self.section_2_3()
        self.section_2_4()
        # self.section_2_5()
        self.section_2_6()
