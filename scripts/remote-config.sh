# returns 0 if instance is ready for write
get_instance_status() {
    read STATUS iSTATUS sSTATUS < <( \
      aws ec2 describe-instance-status \
        --instance-ids "$1" | \
      jq -r ".InstanceStatuses[0].InstanceState.Code,
             .InstanceStatuses[0].InstanceStatus.Details[0].Status,
             .InstanceStatuses[0].SystemStatus.Details[0].Status"
    )

    # make sure instance is running and ready for scp
    if [ "$STATUS" == 16 ] && [ "$iSTATUS" == "passed" ] && [ "$sSTATUS" == "passed" ]; then
      return 0
    fi
    return 1
}

# begin t2.nano instance and save the instance ID
read INSTANCE_ID < <( \
  aws ec2 run-instances \
    --image-id ami-0469b7ed3b974fd81 \
    --count 1 \
    --instance-type t2.nano \
    --key-name main \
    --security-group-ids sg-0b5d1083e0158defe | \
  jq -r '.Instances[0].InstanceId'
)
#echo "$INSTANCE_ID"
#
## make sure the damn thing is ready to be copied into
#while [ "$(get_instance_status "$INSTANCE_ID")" ]; do
#    sleep 5
#    echo "Waiting for state"
#done
#
aws ssm send-command \
    --document-name "AWS-RunRemoteScript" \
    --targets "Key=instanceids,Values=$INSTANCE_ID" \
    --parameters '{"sourceType":["S3"],"sourceInfo":["{\"path\":\"https://minecraft-modded.s3.us-east-2.amazonaws.com/config-ec2.sh\"}"],"commandLine":["bash config-ec2.sh rootkey-4.csv"]}'
