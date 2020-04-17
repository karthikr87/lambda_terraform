import boto3, json

class AWS_Services(object):
    """docstring for AWS_Services."""

    def __init__(self):
        super(AWS_Services, self).__init__()
        self.ec2_client = boto3.client('ec2')
        self.SGid = None
        self.SGIpPermissions = None
        self.quelys_SG = None

    def get_SG_id(self, sg_name):
        self.quelys_SG = self.ec2_client.describe_security_groups(Filters=[{"Name": "group-name", "Values": [sg_name]}, ], )
        for securityGroup in self.quelys_SG['SecurityGroups']:
            self.SGid = securityGroup['GroupId']
            self.SGIpPermissions = securityGroup['IpPermissions']
        return self.SGid


def main():
    aws_Services = AWS_Services()
    sg_id = aws_Services.get_SG_id('MyTestGroup')

    if sg_id:
        attach_sg_to_instance(aws_Services, instance_id, sg_id)

def attach_sg_to_instance(aws_Services, instance_id, sg_id):
    try:
        instance_details = aws_Services.ec2_client.describe_instances(Filters=[{'Name': 'instance-id', 'Values': [instance_id]},],)
        for reservation in instance_details['Reservations']:
                for instance in reservation['Instances']:
                    sg_count = instance['SecurityGroups']
                    if len(sg_count) < 5:
                        aws_Services.ec2_client.modify_instance_attribute(InstanceId=instance_id,Groups=[sg_id])
                        print("SG added")
                    else:
                        modified_sg = sg_count[0]
                        print("adding rule {}".format(rule))
                        for rule in aws_Services.SGIpPermissions:
                            for ip_ranges in rule['IpRanges']:
                                print(ip_ranges)
                                try:
                                    aws_Services.ec2_client.authorize_security_group_ingress(
                                            GroupId=sg_id,
                                            IpPermissions=[
                                                {
                                                    'FromPort': rule['FromPort'],
                                                    'IpProtocol': rule['IpProtocol'],
                                                    'IpRanges': [ip_ranges],
                                                    'ToPort': rule['ToPort'],
                                                    'Ipv6Ranges': rule['Ipv6Ranges'],
                                                    'PrefixListIds': rule['PrefixListIds'],
                                                    'UserIdGroupPairs': rule['UserIdGroupPairs']
                                                },
                                            ],
                                            )

                                except Exception as e:
                                    print(str(e))
                                    print("rule exists. Skipping it")
    except Exception as e:
        print("rule already exists. Skipping")

def handler(event, context):
    print("Received event from cloud watch: " + json.dumps(event, indent=2))

if __name__ == '__main__':
    main()
