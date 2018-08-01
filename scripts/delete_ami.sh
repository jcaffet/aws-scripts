#!/bin/bash
# This script simply deregister a single AMI and delete its related snapshot(s)


usage(){ 
    echo "Usage: $0 <ami_id>" 
    echo "ami_id : id of the AMI to deregister" 
} 

if [ $# -eq 1 ]; then
   ami_id=$1
else
   usage;
   exit 1;
fi

snaps=$(aws ec2 describe-images --image-ids "${ami_id}" --query 'Images[*].BlockDeviceMappings[*].Ebs.SnapshotId' --output text)
echo "Let's deregister AMI ${ami_id} and its snaps : ${snaps}"


echo "Deregister AMI ${ami_id}"
aws ec2 deregister-image --image-id ${ami_id}

for snap in ${snaps}; do
   echo "Delete snapshot ${snap}"
   aws ec2 delete-snapshot --snapshot-id ${snap}
done

