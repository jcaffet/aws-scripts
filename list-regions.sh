#!/bin/sh
# List all active regions

regions=`aws ec2 describe-regions | jq -r '.Regions[] | .RegionName'`

echo ${regions}

