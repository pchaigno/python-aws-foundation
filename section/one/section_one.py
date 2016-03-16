# -*- coding : utf8 -*-

from datetime import datetime

index_user = 0
index_arn = 1
index_user_creation_time = 2
index_password_enabled = 3
index_password_last_used = 4
index_password_last_changed = 5
index_password_next_rotation = 6
index_mfa_active = 7
index_access_key_1_active = 8
index_access_key_1_last_rotated = 9
index_access_key_1_last_used_date = 10
index_access_key_1_last_used_region = 11
index_access_key_1_last_used_service = 12
index_access_key_2_active = 13
index_access_key_2_last_rotated = 14
index_access_key_2_last_used_date = 15
index_access_key_2_last_used_region = 16
index_access_key_2_last_used_service = 17
index_cert_1_active = 18
index_cert_1_last_rotated = 19
index_cert_2_active = 20
index_cert_2_last_rotated = 21


class SectionOne:

    def __init__(self, IAM):
        self.IAM = IAM

    def compare_date(self, older_date, newest_date):
        older_date = datetime.strptime(older_date.split("T")[0], "%Y-%m-%d")
        return older_date - newest_date

    def section_1_1(self):
        self.name = "1.1 Avoid the use of the \"root\" account"
        self.scored = True
        self.passed = True
        for row in self.IAM.credReport:
            if "root_account" in row[index_user]:
                self.passed = False
                break
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_2(self):
        self.name = "1.2 Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console password"
        self.scored = True
        self.passed = True
        for row in self.IAM.credReport:
            if "false" in row[index_mfa_active]:
                self.passed = False
                break
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_3(self):
        self.name = "1.3 Ensure credentials unused for 90 days or greater are disabled"
        self.scored = True
        self.passed = True
        for row in self.IAM.credReport:
            if "true" in row[index_password_enabled]:
                delta = self.compare_date(
                    row[index_password_last_changed],
                    datetime.now()
                )
                if delta.days > 90:
                    self.passed = False
                    break

        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_4(self):
        self.name = "1.4 Ensure access keys are rotated every 90 days or less"
        self.scored = True
        self.passed = True
        for row in self.IAM.credReport:
            if "true" in row[index_access_key_1_active]:
                delta = self.compare_date(
                    row[index_access_key_1_last_rotated],
                    datetime.now()
                )
                if delta.days > 90:
                    self.passed = False
                    break
            if "true" in row[index_access_key_2_active]:
                delta = self.compare_date(
                    row[index_access_key_2_last_rotated],
                    datetime.now()
                )
                if delta.days > 90:
                    self.passed = False
                    break
        print("{}, passed : {}".format(self.name, self.passed))

    def cis_check(self):
        self.section_1_1()
        self.section_1_2()
        self.section_1_3()
        self.section_1_4()
