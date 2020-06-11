import sys
import time
import boto3


ecs_client = boto3.client('ecs')
ec2_client = boto3.client('ec2')


def get_number_ecs_instances_by_cluster(cluster_name):
    num = 0
    paginator = ecs_client.get_paginator('list_container_instances')
    for list_resp in paginator.paginate(cluster=cluster_name):
        num = num + len(list_resp['containerInstanceArns'])
    return num


def find_ecs_instances_by_cluster(cluster_name):
    paginator = ecs_client.get_paginator('list_container_instances')
    for list_resp in paginator.paginate(cluster=cluster_name):
        arns = list_resp['containerInstanceArns']
        desc_resp = ecs_client.describe_container_instances(cluster=cluster_name,
                                                            containerInstances=arns)
    return desc_resp['containerInstances']


def display_ecs_instances(container_instances):
    for container_instance in container_instances:
        display_ecs_instance(container_instance)


def display_ecs_instance(container_instance):
    print('arn=%s, id=%s, status=%s, runningTasksCount=%s' % (container_instance['containerInstanceArn'],
                                                              container_instance['ec2InstanceId'],
                                                              container_instance['status'],
                                                              container_instance['runningTasksCount']))


def rolling_restart_cluster_instances(cluster_name, ecs_instances):
    if is_all_active_instances(ecs_instances):
        for ecs_instance in ecs_instances:
            restart_active_ecs_instance(ecs_instance, cluster_name)
    else:
        print("Not all the instances of %s are in ACTIVE status" % (cluster_name))


def restart_active_ecs_instance(container_instance, cluster_name):
    if container_instance['status'] == "ACTIVE":
        print("Update %s to DRAINING" % (container_instance['containerInstanceArn']))
        ecs_client.update_container_instances_state(
            cluster=cluster_name,
            containerInstances=[container_instance['containerInstanceArn']],
            status='DRAINING')
        running_tasks_count = container_instance['runningTasksCount']
        # wait until there is no more taks running on the instance
        while running_tasks_count != 0:
            container_dict = ecs_client.describe_container_instances(cluster=cluster_name,
                                                                     containerInstances=[container_instance['containerInstanceArn']])
            running_tasks_count = container_dict['containerInstances'][0]['runningTasksCount']
            print("%s runningTasksCount : %s" % (container_instance['containerInstanceArn'],
                                                 running_tasks_count))
            time.sleep(10)
        if running_tasks_count == 0:
            initial_num_instances = get_number_ecs_instances_by_cluster(cluster_name)
            print("Terminate instance %s" % (container_instance['ec2InstanceId']))
            ec2_client.terminate_instances(InstanceIds=[container_instance['ec2InstanceId']])
            # wait to ensure the terminated instance is out of the ECS instances pool
            time.sleep(10)
            # wait until the new instance joins the cluster
            while get_number_ecs_instances_by_cluster(cluster_name) != initial_num_instances:
                print("Waiting until ECS instances number is back to %s" % (initial_num_instances))
                time.sleep(10)


def is_all_active_instances(ecs_instances):
    '''
    Return True is all the ECS instances are in ACTIVE status
    '''
    for ecs_instance in ecs_instances:
        if ecs_instance['status'] != "ACTIVE":
            return False
    return True


def main(argv):
    if len(argv) == 1:
        cluster_name = argv[0]
        print("Cluster %s instances :" % (cluster_name))
        ecs_instances = find_ecs_instances_by_cluster(cluster_name)
        print("Number of instances : %s" % (get_number_ecs_instances_by_cluster(cluster_name)))
        display_ecs_instances(ecs_instances)
        rolling_restart_cluster_instances(cluster_name, ecs_instances)
    else:
        print("Wrong argument number")


if __name__ == "__main__":
    main(sys.argv[1:])
