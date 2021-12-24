aws ssm send-command \
    --document-name "AWS-RunRemoteScript" \
    --targets "Key=instanceids,Values=i-007305afd38ea0c1e" \
    --parameters '{"sourceType":["S3"],"sourceInfo":["{\"path\":\"https://minecraft-modded.s3.us-east-2.amazonaws.com/config-ec2.sh\"}"],"commandLine":["bash config-ec2.sh rootkey-4.csv"]}'