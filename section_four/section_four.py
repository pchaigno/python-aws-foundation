#!/usr/bin/env python2
# -*- coding : utf8 -*-

import boto3

def init_ec2():
    session = boto3.session.Session()
    return session.resource('ec2')


def list_all_tags():
    ec2 = init_ec2()
    for i in ec2.instances.all():
        if i.tags is None:
            continue
        for t in i.tags:
            print("instance id : {}, with tags : {}".format(i,t))

def list_all_sg():
    ec2= init_ec2()
    sglist=[]
    for i in ec2.instances.all():
        for sg in i.security_groups:
            #print sg['GroupId']
            sglist.append(sg)
    return sglist

def list_all_sgId():
    ec2= init_ec2()
    idlist=[]
    for i in ec2.instances.all():
        for sg in i.security_groups:
            #print sg['GroupId']
            idlist.append(sg['GroupId'])
    return idlist
        #print("instance id : {}, with security_groups : {}".format(i,i.security_groups))

# def check_inbound_ssh():
#     sglist=list_all_sg()
#     for sg in sglist:
#         #[{u'GroupName': 'launch-wizard-2', u'GroupId': 'sg-3e2e2a5a'}]
#         responses=[]

def getrules():
    # sglist=list_all_sg()
    ec2=init_ec2()
    rules=[]
    for x in list_all_sgId():
        y=ec2.SecurityGroup(id=x)
        #print y.ip_permissions
        rules.append(y.ip_permissions)
        # rules.update(y.ip_permissions)
    #ec2.SecurityGroup(id=)
    return rules

#ec2c.authorize_security_group_ingress

#     response = client.describe_instances

#     return response


# def get_vm(vm_id):
#     response = client.describe_instances


# def list_sg(vm):
# print repr(vm.security_groups)
# return vm.security_groups


# def test():
# vm id : "i-8af09400"
# ec2 = boto3.resource('ec2')
# vm = ec2.Instance(ins1)
# try:
# list_sg(ins1)
# except:
# print("listing security_groups from vm with id %s ") % (ins1)
