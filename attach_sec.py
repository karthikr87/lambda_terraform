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


def main(instance_id):
    aws_Services = AWS_Services()
    sg_id = aws_Services.get_SG_id('MyTestGroup')

    if sg_id:
        attach_sg_to_instance(aws_Services, instance_id, sg_id)

def attach_sg_to_instance(aws_client, instance_id, sg_id):
    try:
        instance_details = aws_client.ec2_client.describe_instances(Filters=[{'Name': 'instance-id', 'Values': [instance_id]},],)
        for reservation in instance_details['Reservations']:
                for instance in reservation['Instances']:
                    sg_count = instance['SecurityGroups']
                    if len(sg_count) < 5:
                        aws_client.ec2_client.modify_instance_attribute(InstanceId=instance_id,Groups=[sg_id])
                        print("SG added")
                    else:
                        modified_sg = sg_count[0]
                        aws_client.ec2_client.authorize_security_group_ingress(GroupId=modified_sg['GroupId'], IpPermissions=aws_client.SGIpPermissions)
                        print("sg modified")
    except Exception as e:
        print("rule already exists. Skipping")

def handler(event, context):
    print("Received event from cloud watch: " + json.dumps(event, indent=2))
