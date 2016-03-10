#!/usr/bin/env python2
# -*- coding : utf8 -*-

import boto3


def init_ec2():
    session = boto3.session.Session()
    return session.resource('ec2')

def list_all_sg():
    ec2 = init_ec2()
    sglist = []
    for i in ec2.instances.all():
        for sg in i.security_groups:
            # print sg['GroupId']
            sglist.append(sg)
    return sglist

def list_all_sgId():
    ec2 = init_ec2()
    idlist = []
    for i in ec2.instances.all():
        for sg in i.security_groups:
            # print sg['GroupId']
            idlist.append(sg['GroupId'])
    return idlist

def getrules():
    # sglist=list_all_sg()
    ec2 = init_ec2()
    rules = []
    for x in list_all_sgId():
        y = ec2.SecurityGroup(id=x)
        rules += y.ip_permissions
        # rules.update(y.ip_permissions)
    return rules


def filterSSH():
    rules = getrules()
    rezlist = []

    for r in rules:
        if r['ToPort'] != 22:
            continue
        else:
            # r['IpRanges'] contains [{u'CidrIp': '1.1.1.1/23'}]
            rezlist += r['IpRanges'][0].values()
    if '0.0.0.0/0' in rezlist:
        print "forbidden rule is present"
    else: 
        print "test passed"

def filterRDP():
    rules = getrules()
    rezlist = []

    for r in rules:
        if r['ToPort'] != 3389:
            continue
        else:
            # r['IpRanges'] contains [{u'CidrIp': '1.1.1.1/23'}]
            rezlist += r['IpRanges'][0].values()
    if '0.0.0.0/0' in rezlist:
        print "forbidden rule is present"
    else: 
        print "test passed"
