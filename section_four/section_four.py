#!/usr/bin/env python2
# -*- coding : utf8 -*-

import boto3


class SectionFour(object):
    """CIS-AWS section 4: Networking"""

    def __init__(self):
        self.session = boto3.session.Session()
        self.ec2 = self.session.resource('ec2')

    def list_all_sg(self):
        sglist = []
        for i in self.ec2.instances.all():
            for sg in i.security_groups:
                # print sg['GroupId']
                sglist.append(sg)
        return sglist

    def list_all_sgId(self):
        idlist = []
        for i in self.ec2.instances.all():
            for sg in i.security_groups:
                # print sg['GroupId']
                idlist.append(sg['GroupId'])
        return idlist

    def getrules(self):
        # sglist=list_all_sg()
        rules = []
        for x in self.list_all_sgId():
            y = self.ec2.SecurityGroup(id=x)
            rules += y.ip_permissions
            # rules.update(y.ip_permissions)
        return rules

    def section_4_1(self):
        """no ssh from 0.0.0.0/0"""
        self.name = "4.1 Ensure no security groups allow ingress from 0.0.0.0/0 to port 22"
        self.scored = True
        self.passed = True
        rules = self.getrules()
        rezlist = []

        for r in rules:
            if r['ToPort'] != 22:
                continue
            else:
                # r['IpRanges'] contains [{u'CidrIp': '1.1.1.1/23'}]
                rezlist += r['IpRanges'][0].values()
        if '0.0.0.0/0' in rezlist:
            # print "forbidden rule is present"
            self.passed = False
        else:
            print("{}, passed : {}".format(self.name, self.passed))

    def section_4_2(self):
        """no RDP from 0.0.0.0/0"""
        self.name = "4.2 Ensure no security groups allow ingress from 0.0.0.0/0 to port 3389"
        self.scored = True
        self.passed = True
        rules = self.getrules()
        rezlist = []

        for r in rules:
            if r['ToPort'] != 3389:
                continue
            else:
                # r['IpRanges'] contains [{u'CidrIp': '1.1.1.1/23'}]
                rezlist += r['IpRanges'][0].values()
        if '0.0.0.0/0' in rezlist:
            # print "forbidden rule is present"
            self.passed = False
        else:
            print("{}, passed : {}".format(self.name, self.passed))
