#!/usr/bin/python
#
# This scripts provides a list of ELBv1 loadbalancers with their connection draining information
# Display : LoadBalancerName;ConnectionDraining_Enabled;ConnectionDraining_Timeout

import boto3
import sys

def main(argv):

   load_balancers = list_all_load_balancers()

   for load_balancer in load_balancers:
      lb_name = load_balancer.get('LoadBalancerName')
      lb_connection_draining = get_lb_connection_draining(lb_name)
      print("%s;%s;%s" % (lb_name, lb_connection_draining.get('Enabled'), lb_connection_draining.get('Timeout')))

def list_all_load_balancers():
   client = boto3.client('elb')
   response = client.describe_load_balancers()
   return response.get('LoadBalancerDescriptions')

def get_lb_connection_draining(lb_name):
   client = boto3.client('elb')
   response = client.describe_load_balancer_attributes(LoadBalancerName=lb_name)
   attributes = response.get('LoadBalancerAttributes')
   return attributes.get('ConnectionDraining')

if __name__ == '__main__':
    main(sys.argv[1:])

