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
        #
        # TODO: check for the value in
        # - password_last_used
        # - access_key_1_last_used_date
        # - access_key_2_last_used_date
        #
        for row in self.IAM.credReport:
            if "root_account" in row[index_user]:
                self.passed = False
                break
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_2(self):
        self.name = "1.2 Ensure multi-factor authentication (MFA) is enabled for all IAM users that have a console password"
        self.scored = True
        self.passed = True
        #
        # This test might not work, for some not yet known reasons.
        # mfa_active is still false, even if i setup a virtual MFA on my root
        # account.
        # trying to generate_credential_report() doesn't seems to update the
        # value
        #
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

    def section_1_5(self):
        self.name = "1.5 Ensure IAM password policy requires at least one uppercase letter"
        self.scored = True
        self.passed = False
        if self.IAM.passwordPolicy is not None:
                self.passed = self.IAM.passwordPolicy["RequireUppercaseCharacters"]
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_6(self):
        self.name = "1.6 Ensure IAM password policy requires at least one lowercase letter"
        self.scored = True
        self.passed = False
        if self.IAM.passwordPolicy is not None:
                self.passed = self.IAM.passwordPolicy["RequireLowercaseCharacters"]
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_7(self):
        self.name = "1.7 Ensure IAM password policy requires at least one symbol"
        self.scored = True
        self.passed = False
        if self.IAM.passwordPolicy is not None:
                self.passed = self.IAM.passwordPolicy["RequireSymbols"]
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_8(self):
        self.name = "1.8 Ensure IAM password policy requires at least one number"
        self.scored = True
        self.passed = False
        if self.IAM.passwordPolicy is not None:
                self.passed = self.IAM.passwordPolicy["RequireNumbers"]
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_9(self):
        self.name = "1.9 Ensure IAM password policy requires minimum length of 14 or greater"
        self.scored = True
        self.passed = False
        if self.IAM.passwordPolicy is not None:
            if self.IAM.passwordPolicy["MinimumPasswordLength"] >= 14:
                self.passed = True
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_10(self):
        self.name = "1.10 Ensure IAM password policy prevents password reuse"
        self.scored = True
        self.passed = False
        if self.IAM.passwordPolicy is not None:
            if "PasswordReusePrevention" in self.IAM.passwordPolicy:
                if self.IAM.passwordPolicy["PasswordReusePrevention"] >= 24:
                    self.passed = True
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_11(self):
        self.name = "1.11 Ensure IAM password policy expires passwords within 90 days or less "
        self.scored = True
        self.passed = False
        if self.IAM.passwordPolicy is not None:
            if "MaxPasswordAge" in self.IAM.passwordPolicy:
                if self.IAM.passwordPolicy["MaxPasswordAge"] <= 90:
                    self.passed = True
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_12(self):
        self.name = "1.12 Ensure no root account access key exists"
        self.scored = True
        self.passed = False
        for row in self.IAM.credReport:
            if "root_account" in row[index_user]:
                if (
                    (row[index_access_key_1_active] == "false") and
                    (row[index_access_key_2_active] == "false")
                ):
                    self.passed = True
                break
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_13(self):
        self.name = "1.13 Ensure hardware MFA is enabled for the \"root\" account"
        self.scored = True
        self.passed = False
        #
        # This test is not properly described in the CIS AWS Foundation
        #
        # Run the following command:
        # aws iam get-account-summary
        # Ensure the AccountMFAEnabled property is set to 1
        #
        # This doesn't check if the MFA is enabled for the root account or for
        # an other user
        print("{}, passed : {}".format(self.name, self.passed))

    def section_1_14(self):
        self.name = """1.14 Ensure security questions are registered in the AWS account.
        Manually perform this test"""
        self.scored = False
        self.passed = False
        #
        # This test is automatable
        #
        print("{}, scored : {}".format(self.name, self.scored))

    def section_1_15(self):
        self.name = "1.15 Ensure IAM policies are attached only to groups or roles"
        self.scored = True
        self.passed = True
        for user in self.IAM.users:
            attachedPolicies = self.IAM.getUserAttachedPolicies(user["UserName"])
            userPolicies = self.IAM.getUserPolicies(user["UserName"])
            if (attachedPolicies or userPolicies):
                self.passed = False
        print("{}, passed : {}".format(self.name, self.passed))

    def cis_check(self):
        self.section_1_1()
        self.section_1_2()
        self.section_1_3()
        self.section_1_4()
        self.section_1_5()
        self.section_1_6()
        self.section_1_7()
        self.section_1_8()
        self.section_1_9()
        self.section_1_10()
        self.section_1_11()
        self.section_1_12()
        self.section_1_13()
        self.section_1_14()
        self.section_1_15()
