#!/usr/bin/python
#
# This scripts lists all the EC2 load balancers of an account
# This includes :
# - classic load balancers (through ElasticLoadBalancing)
# - application and network load balancers (through ElasticLoadBalancingv2)
# Display : LoadBalancerName

import boto3
import sys

def main(argv):

   all_load_balancers_names = set().union(list_all_load_balancers_names(), \
                                          list_all_load_balancersv2_names())

   for load_balancer in all_load_balancers_names:
      print("%s" % (load_balancer))

def list_all_load_balancers_names():
   client = boto3.client('elb')
   response = client.describe_load_balancers()
   descriptions = response.get('LoadBalancerDescriptions')
   return list([description.get('LoadBalancerName') for description in descriptions])

   return description.get('LoadBalancerName')

def list_all_load_balancersv2_names():
   client = boto3.client('elbv2')
   response = client.describe_load_balancers()
   load_balancers = response.get('LoadBalancers')
   return list([load_balancer.get('LoadBalancerName') for load_balancer in load_balancers])

if __name__ == '__main__':
    main(sys.argv[1:])

