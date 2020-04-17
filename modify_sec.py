import boto3, json

class AWS_Services(object):
    """docstring for AWS_Services."""

    def __init__(self):
        super(AWS_Services, self).__init__()
        self.ec2_client = boto3.client('ec2')
        self.SGid = None
        self.SGIpPermissions = None

    def get_SG_id(self, sg_name):
        groups = self.ec2_client.describe_security_groups(Filters=[{"Name": "group-name", "Values": [sg_name]}, ], )
        for securityGroup in groups['SecurityGroups']:
            self.SGid = securityGroup['GroupId']
            self.SGIpPermissions = securityGroup['IpPermissions']
        return self.SGid

def main():
    aws_Services = AWS_Services()
    sg_id = aws_Services.get_SG_id('instance_SG')
    merge_sec_group = aws_Services.ec2_client.describe_security_groups(Filters=[{"Name": "group-name", "Values": ["ssh_SG"]}, ], )
    for securityGroup in merge_sec_group['SecurityGroups']:
        ip_permissions = securityGroup['IpPermissions']
        print(ip_permissions)
        for rule in ip_permissions:
            print(len(rule['IpRanges']))
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




        # for rule in ip_permissions:
        #     try:
        #         aws_Services.ec2_client.authorize_security_group_ingress(
        #                 GroupId=sg_id,
        #                 IpPermissions=[
        #                     {
        #                         'FromPort': rule['FromPort'],
        #                         'IpProtocol': rule['IpProtocol'],
        #                         'IpRanges': rule['IpRanges'],
        #                         'ToPort': rule['ToPort'],
        #                         'Ipv6Ranges': rule['Ipv6Ranges'],
        #                         'PrefixListIds': rule['PrefixListIds'],
        #                         'UserIdGroupPairs': rule['UserIdGroupPairs']
        #                     },
        #                 ],
        #                 )
        #
        #     except Exception as e:
        #         print(str(e))
        #         print("rule exists. Skipping it")


if __name__ == '__main__':
    main()
