# -*- coding : utf8 -*-

from json import loads
from dateutil.tz import tzlocal
from datetime import datetime


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
            S3BucketPolicy = self.S3.getS3BucketPolicy(self.S3.CTBucketName)
            # temporary fix, waiting for
            # https://github.com/aws/aws-cli/issues/1851
            S3BucketPolicy = loads(S3BucketPolicy["Policy"])
            for statement in S3BucketPolicy["Statement"]:
                if (statement["Effect"] == "Allow" and
                        statement["Principal"] == "*"):
                    self.passed = False
        else:
            # there is no S3 bucket used to store cloudtrail logs, so it can
            # not be publicly accessible, but we consider this test as failed
            self.passed = False
        print("{}, passed : {}".format(self.name, self.passed))

    # def section_2_4(self):
        self.name = "2.4 Ensure CloudTrail trails are integrated with CloudWatch Logs"
        self.scored = True
        self.passed = True

        if self.CT.describe_trails() is not None:
            resp = self.CT.describe_trails()

            if u'CloudWatchLogsRoleArn' in resp["trailList"][0].keys():
                CWname = resp["trailList"][0][u'Name']
                CWstatus = self.CT.get_trail_status(Name=CWname)

                if CWstatus[u'IsLogging']:
                    LastDelivery = CWstatus[
                        u'LatestCloudWatchLogsDeliveryTime']
                    delta = datetime.now(tzlocal()) - LastDelivery
                    if delta.days > 1:
                        # logs are considered too old, integration test is
                        # failed
                        self.passed = False
                else:
                    # currently not Logging
                    self.passed = False
            else:  # no CloudWatch integration
                self.passed = False

        else:
            # problem with describe_trails
            self.passed = False

        print("{}, passed : {}".format(self.name, self.passed))

    def cis_check(self):
        self.section_2_1()
        self.section_2_2()
        self.section_2_3()
