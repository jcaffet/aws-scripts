#!/bin/sh

PYTHON_EXEC=python3.7

${PYTHON_EXEC} rds/list_rds_instances.py >report_list_rds_instances.csv
${PYTHON_EXEC} ec2/list_instances.py >report_list_instances.csv
${PYTHON_EXEC} ebs/list_ebs_volumes.py >report_list_ebs_volumes.csv
${PYTHON_EXEC} ami/list_own_ami.py >report_list_own_ami.csv
${PYTHON_EXEC} ami/list_instances_with_unvisible_ami.py >report_list_instances_with_unvisible_ami.csv
${PYTHON_EXEC} asg/list_asg.py >report_list_asg.csv
${PYTHON_EXEC} ssm/list_managed_instances.py > report_list_managed_instances.csv
${PYTHON_EXEC} vpc/list_unused_security_groups.py > report_list_unused_security_groups.txt
${PYTHON_EXEC} iam/list_iam_users_old_password.py > report_list_iam_users_old_password.csv
${PYTHON_EXEC} iam/list_inactive_iam_users.py > report_list_inactive_iam_users.csv
