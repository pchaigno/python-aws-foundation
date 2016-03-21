# -*- coding : utf8 -*-


class SectionFour:

    def __init__(self, EC2):
        self.EC2 = EC2

    def section_4_1(self):
        self.name = "4.1 Ensure no security groups allow ingress from 0.0.0.0/0 to port 22"
        self.scored = True
        self.passed = True
        for rule in self.EC2.securityGroups:
            for permission in rule["IpPermissions"]:
                if (
                        ("ToPort" in permission) and
                        (permission["ToPort"] == 22) and
                        ({u'CidrIp': '0.0.0.0/0'} in permission["IpRanges"])
                        ):
                    self.passed = False
        print("{}, passed : {}".format(self.name, self.passed))

    def section_4_2(self):
        self.name = "4.2 Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389"
        self.scored = True
        self.passed = True
        for rule in self.EC2.securityGroups:
            for permission in rule["IpPermissions"]:
                if (
                        ("ToPort" in permission) and
                        (permission["ToPort"] == 3389) and
                        ({u'CidrIp': '0.0.0.0/0'} in permission["IpRanges"])
                        ):
                    self.passed = False
        print("{}, passed : {}".format(self.name, self.passed))

    def section_4_3(self):
        self.name = "4.3 Ensure VPC Flow Logging is Enabled in all Applicable Regions"
        self.scored = True
        self.passed = False
        for flow in self.EC2.flowLogs:
            if flow["FlowLogStatus"] == "ACTIVE":
                self.passed = True
                break
        print("{}, passed : {}".format(self.name, self.passed))

    def section_4_4(self):
        self.name = "4.4 Ensure the default security group restricts all traffic"
        self.scored = True
        self.passed = True
        for rule in self.EC2.securityGroups:
            if (
                rule["IpPermissions"] and
                rule["IpPermissionsEgress"]
            ):
                self.passed = False
        print("{}, passed : {}".format(self.name, self.passed))

    def cis_check(self):
        self.section_4_1()
        self.section_4_2()
        self.section_4_3()
        self.section_4_4()
