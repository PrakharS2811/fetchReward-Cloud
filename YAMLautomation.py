#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 23 20:15:46 2021

@author: prakhar
"""
import yaml
import boto3


ec2 = boto3.client('ec2')


a_yaml_file = open("/home/prakhar/Programming/fetch-rewardsd/Template.yaml")
parsed_yaml_file = yaml.load(a_yaml_file, Loader=yaml.FullLoader)

resources=parsed_yaml_file.get("Resources")

EC2Instance=resources.get("EC2Instance")

Properties=EC2Instance.get("Properties")
print(Properties.get("ImageId"))


BlockDeviceMapping=Properties.get("BlockDeviceMappings")

FirstVolume=BlockDeviceMapping[0].get("Ebs")
SecondVolume=BlockDeviceMapping[1].get("Ebs")
print(Properties.get("KeyName"))



response = ec2.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': BlockDeviceMapping[0].get("DeviceName"),
            'Ebs': {
                'DeleteOnTermination':False,
                'Iops': int(FirstVolume.get("Iops")),
                'VolumeSize': int(FirstVolume.get("VolumeSize")),
                'VolumeType': FirstVolume.get("VolumeType"),
            }
            },
            {
           'DeviceName': BlockDeviceMapping[1].get("DeviceName"),
            'Ebs': {
                'DeleteOnTermination':False,
                'Iops': int(SecondVolume.get("Iops")),
                'VolumeSize': int(SecondVolume.get("VolumeSize")),
                'VolumeType': SecondVolume.get("VolumeType"),
            }
        },
    ],
    KeyName=Properties.get("KeyName"),
    UserData = '''
    #!/bin/bash
    useradd user1
    useradd user2
    ''',
    MaxCount=1,
    MinCount=1,
    ImageId=Properties.get("ImageId"),
    InstanceType=Properties.get("InstanceType")
)
print("Instance Created")
print(response)
print('\nrespose:  '+response["Instances"][0]["InstanceId"])



