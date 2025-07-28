# 🚀 AWS ECS Fargate Deployment Guide for Radio Sahoo

## Prerequisites Setup

### 1. Create ECR Repository (Manual Step Required)
Since the current AWS user lacks ECR permissions, create the repository manually:

**AWS Console Method:**
1. Go to [AWS ECR Console](https://console.aws.amazon.com/ecr/)
2. Click "Create repository"
3. Repository name: `radio-sahoo`
4. Leave other settings as default
5. Click "Create repository"
6. Note the repository URI: `896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo`

### 2. Create Required IAM Roles

**ECS Task Execution Role:**
```bash
aws iam create-role --role-name ecsTaskExecutionRole \
  --assume-role-policy-document file://aws-setup-roles.json

aws iam attach-role-policy --role-name ecsTaskExecutionRole \
  --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

**ECS Task Role:**
```bash
aws iam create-role --role-name ecsTaskRole \
  --assume-role-policy-document file://aws-setup-roles.json
```

### 3. Create CloudWatch Log Group
```bash
aws logs create-log-group --log-group-name /ecs/radio-sahoo --region ap-southeast-2
```

### 4. Get Default VPC and Subnet Information
```bash
# Get default VPC
aws ec2 describe-vpcs --filters "Name=is-default,Values=true" --region ap-southeast-2

# Get subnets in default VPC
aws ec2 describe-subnets --filters "Name=vpc-id,Values=vpc-xxxxxx" --region ap-southeast-2

# Get default security group
aws ec2 describe-security-groups --filters "Name=group-name,Values=default" --region ap-southeast-2
```

## Deployment Steps

### Step 1: Build and Push Docker Image
```bash
# Run the deployment script
./aws-deploy.sh
```

### Step 2: Update Network Configuration
Edit `aws-deploy.sh` and replace the network configuration with your actual values:
```bash
--network-configuration "awsvpcConfiguration={subnets=[subnet-12345,subnet-67890],securityGroups=[sg-abcdef],assignPublicIp=ENABLED}"
```

### Step 3: Deploy to ECS
```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name radio-sahoo-cluster --region ap-southeast-2

# Register task definition
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json --region ap-southeast-2

# Create service (after updating network config)
aws ecs create-service \
  --cluster radio-sahoo-cluster \
  --service-name radio-sahoo-service \
  --task-definition radio-sahoo-task:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[YOUR_SUBNET_IDS],securityGroups=[YOUR_SECURITY_GROUP_ID],assignPublicIp=ENABLED}" \
  --region ap-southeast-2
```

## Optional: Application Load Balancer Setup

### Create Application Load Balancer
```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name radio-sahoo-alb \
  --subnets subnet-12345 subnet-67890 \
  --security-groups sg-abcdef \
  --region ap-southeast-2

# Create target group
aws elbv2 create-target-group \
  --name radio-sahoo-targets \
  --protocol HTTP \
  --port 5000 \
  --vpc-id vpc-xxxxxx \
  --target-type ip \
  --health-check-path /health \
  --region ap-southeast-2

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:... \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:...
```

### Update ECS Service with Load Balancer
```bash
aws ecs update-service \
  --cluster radio-sahoo-cluster \
  --service radio-sahoo-service \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:...,containerName=radio-sahoo,containerPort=5000 \
  --region ap-southeast-2
```

## Security Considerations

### 1. Update Security Group Rules
```bash
# Allow HTTP traffic on port 80
aws ec2 authorize-security-group-ingress \
  --group-id sg-abcdef \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

# Allow application port 5000 (if ALB is used)
aws ec2 authorize-security-group-ingress \
  --group-id sg-abcdef \
  --protocol tcp \
  --port 5000 \
  --source-group sg-abcdef
```

### 2. Environment Variables
Update `aws-task-definition.json` with:
- Secure `SECRET_KEY` (use AWS Secrets Manager for production)
- Proper database configuration
- Any other environment-specific settings

## Monitoring and Logs

### View ECS Service Status
```bash
aws ecs describe-services \
  --cluster radio-sahoo-cluster \
  --services radio-sahoo-service \
  --region ap-southeast-2
```

### View CloudWatch Logs
```bash
aws logs describe-log-streams \
  --log-group-name /ecs/radio-sahoo \
  --region ap-southeast-2

aws logs get-log-events \
  --log-group-name /ecs/radio-sahoo \
  --log-stream-name ecs/radio-sahoo/TASK_ID \
  --region ap-southeast-2
```

## Accessing Your Application

After successful deployment:
1. **Without ALB:** Use the public IP of the ECS task on port 5000
2. **With ALB:** Use the ALB DNS name on port 80

Find the public IP:
```bash
aws ecs describe-tasks \
  --cluster radio-sahoo-cluster \
  --tasks $(aws ecs list-tasks --cluster radio-sahoo-cluster --service-name radio-sahoo-service --query 'taskArns[0]' --output text) \
  --region ap-southeast-2
```

## Troubleshooting

### Common Issues:
1. **Task keeps stopping:** Check CloudWatch logs for errors
2. **Cannot reach application:** Verify security group allows inbound traffic
3. **Image pull errors:** Ensure ECR permissions and image exists
4. **Database issues:** Check volume mounts and permissions

### Useful Commands:
```bash
# Check service events
aws ecs describe-services --cluster radio-sahoo-cluster --services radio-sahoo-service --region ap-southeast-2

# View task definition
aws ecs describe-task-definition --task-definition radio-sahoo-task --region ap-southeast-2

# List running tasks
aws ecs list-tasks --cluster radio-sahoo-cluster --service-name radio-sahoo-service --region ap-southeast-2
```

## Cost Optimization

- **Fargate vCPU:** 0.25 vCPU = ~$8/month
- **Fargate Memory:** 0.5 GB = ~$2/month  
- **Data Transfer:** First 1GB free, then $0.09/GB
- **Total Estimated Cost:** ~$10-15/month for basic usage

## Next Steps

1. Set up custom domain with Route 53
2. Configure SSL/TLS with ACM
3. Implement auto-scaling policies
4. Set up monitoring and alerting
5. Consider using RDS for production database

---

**Radio Sahoo AWS Deployment Guide**  
*Version 1.0 - July 2025*

🎵 Ready for cloud-scale music streaming! 🎵