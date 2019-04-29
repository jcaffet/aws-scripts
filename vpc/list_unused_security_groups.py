#!/usr/bin/python
#
# This scripts provides information on *potentially* unused security groups management
# It takes into account security groups of :
# - EC2 instances
# - EC2 load balancers
# - RDS instances
# - Lambda functions
# - Elascticache resources
# - Network Interfaces
# - OpsWorks layers

import boto3
import sys
import time

def main(argv):

   CLOUDTRAIL_RETENTION_LIMIT=90

   sec_groups = list_all_sec_groups()
   all_sg_ids = list_all_sec_group_ids(sec_groups)

   ec2_instances = list_all_ec2_instances()
   all_ec2_sg_ids = list_ec2_sec_group_ids(ec2_instances)

   ec2_load_balancers = list_all_load_balancers()
   all_lb_sg_ids = list_lb_sec_group_ids(ec2_load_balancers)

   rds_instances = list_all_rds_instances()
   all_rds_sg_ids = list_rds_sec_group_ids(rds_instances)

   lambda_functions = list_all_lambdas()
   all_functions_sg_ids = list_lambda_sec_group_ids(lambda_functions)

   elasticaches = list_all_caches()
   all_cache_sg_ids = list_elacticache_sec_group_ids(elasticaches)

   ec2_network_interfaces = list_all_network_interfaces()
   all_eni_sg_ids = list_eni_sec_group_ids(ec2_network_interfaces)

   opsworks_layers = list_all_opsworks_layers()
   all_opsworks_layers_sg_ids = list_opsworks_layers_sec_group_ids(opsworks_layers)

   used_sg_ids = set().union(all_ec2_sg_ids, \
                             all_rds_sg_ids, \
                             all_lb_sg_ids, \
                             all_functions_sg_ids, \
                             all_cache_sg_ids, \
                             all_eni_sg_ids, \
                             all_opsworks_layers_sg_ids)

   unused_sg_ids = set(all_sg_ids) - set(used_sg_ids)

   print ("%s security groups attached %s times to EC2 instances." % (len(set(all_ec2_sg_ids)), len(all_ec2_sg_ids)))
   print ("%s security groups attached %s times to Load Balancers." % (len(set(all_lb_sg_ids)), len(all_lb_sg_ids)))
   print ("%s security groups attached %s times to RDS instances." % (len(set(all_rds_sg_ids)), len(all_rds_sg_ids)))
   print ("%s security groups attached %s times to Lambda functions." % (len(set(all_functions_sg_ids)), len(all_functions_sg_ids)))
   print ("%s security groups attached %s times to Elastic Caches." % (len(set(all_cache_sg_ids)), len(all_cache_sg_ids)))
   print ("%s security groups attached %s times to Network Interfaces." % (len(set(all_eni_sg_ids)), len(all_eni_sg_ids)))
   print ("%s security groups attached %s times to OpsWorks Layers." % (len(set(all_opsworks_layers_sg_ids)), len(all_opsworks_layers_sg_ids)))
   print ("")
   print ("Used security groups : %s" % (len(used_sg_ids)))
   print ("Unused security groups : %s" % (len(unused_sg_ids)))
   print ("Total security groups : %s" % (len(all_sg_ids)))
   print ("")
   print ("Unused security groups for more that %s days details :" % CLOUDTRAIL_RETENTION_LIMIT)
   for sec_group in get_sec_groups(list(unused_sg_ids)):
      events = show_events(sec_group.group_id)
      if len(events) == 0:
         print("%s;%s;%s" % (sec_group.group_id, sec_group.group_name, sec_group.description))
      time.sleep(1)

# Return type : list(ec2.SecurityGroup)
def list_all_sec_groups():
   ec2 = boto3.resource('ec2')
   return ec2.security_groups.all()

def list_all_sec_group_ids(sec_groups):
   return list([sec_group.group_id for sec_group in sec_groups])

def list_all_ec2_instances():
   client = boto3.client('ec2')
   response = client.describe_instances()
   reservations = response['Reservations']
   return list([instance for reservation in reservations for instance in reservation['Instances']])

def list_ec2_sec_group_ids(ec2_instances):
   return list([inst_sec_group.get('GroupId') for ec2_instance in ec2_instances for inst_sec_group in ec2_instance.get('SecurityGroups')])

def list_all_load_balancers():
   client = boto3.client('elb')
   response = client.describe_load_balancers()
   return response.get('LoadBalancerDescriptions')

def list_lb_sec_group_ids(ec2_load_balancers):
   return list([elb_sec_group for elb in ec2_load_balancers for elb_sec_group in elb.get('SecurityGroups')])

def list_all_rds_instances():
   client = boto3.client('rds')
   response = client.describe_db_instances()
   return response.get('DBInstances')

def list_rds_sec_group_ids(rds_instances):
   return list([rds_sec_group['VpcSecurityGroupId'] for rds_instance in rds_instances for rds_sec_group in rds_instance.get('VpcSecurityGroups')])

def list_all_lambdas():
   client = boto3.client('lambda')
   lambdas = client.list_functions()
   return list([lambda_function for lambda_function in lambdas['Functions']])

def list_sec_groups_from_lambda(lambda_function):
   sec_groups = []
   if 'VpcConfig' in lambda_function.keys():
      for sec_group in lambda_function['VpcConfig']['SecurityGroupIds']:
         sec_groups.append(sec_group)
   return sec_groups

def list_sec_groups_from_lambdas(lambda_functions):
   sec_groups = []
   for lambda_function in lambda_functions:
      for sec_group in list_sec_groups_from_lambda(lambda_function):
         sec_groups.append(sec_group)
   return filter(None, sec_groups)

def list_lambda_sec_group_ids(lambda_functions):
   return list([lambda_sec_group for lambda_sec_group in list_sec_groups_from_lambdas(lambda_functions)])

def list_all_caches():
   client = boto3.client('elasticache')
   response = client.describe_cache_clusters()
   return response.get('CacheClusters')

def list_elacticache_sec_group_ids(elasticaches):
   return list([cache_sec_group.get('SecurityGroupId') for cache in elasticaches for cache_sec_group in cache.get('SecurityGroups')])

def list_all_network_interfaces():
   client = boto3.client('ec2')
   response = client.describe_network_interfaces()
   return response.get('NetworkInterfaces')

def list_eni_sec_group_ids(ec2_network_interfaces):
   return list([eni_sec_group['GroupId'] for eni in ec2_network_interfaces for eni_sec_group in eni.get('Groups')])

def list_all_opsworks_layers():
   layers = []
   client = boto3.client('opsworks')
   opsworks_stacks = client.describe_stacks()
   for stack in opsworks_stacks.get("Stacks"):
      layer_iterator = stack.layers.all()
      for layer in layer_iterator:
         layers.append(layer) 
   return layers

def list_opsworks_layers_sec_group_ids(opsworks_layers):
   return list([layer_sec_group for layer in opsworks_layers for layer_sec_group in layer.get('CustomSecurityGroupIds') ])

# Return type : list(ec2.SecurityGroup)
def get_sec_groups(sec_group_ids):
   client = boto3.resource('ec2')
   return client.security_groups.filter(GroupIds=sec_group_ids)

def show_events(sec_group_id):
   client = boto3.client('cloudtrail')
   response = client.lookup_events(
                     LookupAttributes=[
                        {
                         'AttributeKey': 'ResourceName',
                         'AttributeValue': sec_group_id
                        },
                        ],
                     )
   return response.get('Events')

if __name__ == '__main__':
    main(sys.argv[1:])

