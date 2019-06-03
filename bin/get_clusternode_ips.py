#!/usr/bin/env python
import boto3
import argparse
import pprint

def get_clusternode_ips(stack_name, region, logical_id):
    ec2 = boto3.resource('ec2', region_name=region)
    filters = [
            {'Name': 'tag:aws:cloudformation:stack-name', 'Values': [stack_name]},
            {'Name': 'tag:aws:cloudformation:logical-id', 'Values': [logical_id]},
            {'Name': 'instance-state-name', 'Values': ['pending','running']},
        ]
    instance_ips = [i.private_ip_address for i in ec2.instances.filter(Filters=filters)]
    return (instance_ips)


if __name__ == "__main__":
    '''
        get a list of the clusternode ips
        '''

    parser = argparse.ArgumentParser(description='tool to get the ip adresses of the ec2 nodes for a cfn stack')
    parser.add_argument('stack_name', help="name of the stack you want the IP's for", action="store")
    parser.add_argument('region', nargs='?', default="us-east-1", help="defaults to 'us-east-1' but you may want 'us-west-2' instead ", action="store")
    parser.add_argument('logical_id', nargs='?', default="ClusterNodeGroup", help="defaults to 'ClusterNodeGroup' but you may want 'SynchronyClusterNodeGroup' instead ", action="store")
    args = parser.parse_args()

    result = get_clusternode_ips(args.stack_name, args.region, args.logical_id)

    pprint.pprint(result)
