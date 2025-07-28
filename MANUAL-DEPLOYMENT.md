# 📋 Manual AWS ECS Deployment Steps for Radio Sahoo

Since the automated script has permission limitations, follow these manual steps:

## ✅ Prerequisites Completed
- [x] ECR Repository: `896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo`
- [x] Docker image built locally: `radio-sahoo:latest`
- [x] VPC Configuration: `vpc-21332c46`
- [x] Subnets: `subnet-255aab6d`, `subnet-59dd1a3f`, `subnet-5391e70b`
- [x] Security Group: `sg-ffe07db6` (with ports 80, 443, 5000 open)

## 🚀 Step-by-Step Deployment

### Step 1: Push Docker Image to ECR (AWS Console Method)

Since CLI lacks ECR permissions, use AWS Console:

1. **Go to ECR Console:** https://console.aws.amazon.com/ecr/
2. **Select Repository:** `radio-sahoo`
3. **Click "View push commands"**
4. **Run these commands locally:**

```bash
# 1. Get login token (may need console)
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com

# 2. Tag your image
docker tag radio-sahoo:latest 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo:latest

# 3. Push the image
docker push 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo:latest
```

**Alternative:** If CLI doesn't work, manually upload via AWS Console or use a different AWS profile with ECR permissions.

### Step 2: Create CloudWatch Log Group

**AWS Console Method:**
1. Go to CloudWatch Console → Log groups
2. Create log group: `/ecs/radio-sahoo`
3. Region: `ap-southeast-2`

**CLI Method (if permissions allow):**
```bash
aws logs create-log-group --log-group-name /ecs/radio-sahoo --region ap-southeast-2
```

### Step 3: Create IAM Roles for ECS

**AWS Console Method:**
1. Go to IAM Console → Roles
2. Create two roles:

**Role 1: ecsTaskExecutionRole**
- Trust policy: ECS Tasks
- Attach policy: `AmazonECSTaskExecutionRolePolicy`

**Role 2: ecsTaskRole** 
- Trust policy: ECS Tasks
- No additional policies needed for basic deployment

### Step 4: Create ECS Cluster

**AWS Console Method:**
1. Go to ECS Console → Clusters
2. Click "Create Cluster" 
3. Cluster name: `radio-sahoo-cluster`
4. Infrastructure: AWS Fargate (serverless)
5. Create cluster

**CLI Method:**
```bash
aws ecs create-cluster --cluster-name radio-sahoo-cluster --region ap-southeast-2
```

### Step 5: Register Task Definition

**AWS Console Method:**
1. Go to ECS Console → Task Definitions
2. Click "Create new task definition"
3. Task definition family: `radio-sahoo-task`
4. Launch type: AWS Fargate
5. Operating system: Linux/X86_64
6. CPU: 0.25 vCPU
7. Memory: 0.5 GB
8. Task execution role: `ecsTaskExecutionRole`
9. Task role: `ecsTaskRole`

**Container Details:**
- Container name: `radio-sahoo`
- Image URI: `896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo:latest`
- Port: 5000 (TCP)
- Environment variables:
  ```
  FLASK_ENV=production
  FLASK_DEBUG=0
  SECRET_KEY=your-production-secret-key
  DATABASE_PATH=/app/data/radio_sahoo.db
  STREAM_URL=https://d3d4yli4hf5bmh.cloudfront.net/hls/live.m3u8
  METADATA_URL=https://d3d4yli4hf5bmh.cloudfront.net/metadatav2.json
  COVER_ART_URL=https://d3d4yli4hf5bmh.cloudfront.net/cover.jpg
  LOG_LEVEL=INFO
  ```

**Logging:**
- Log driver: awslogs
- Log group: `/ecs/radio-sahoo`
- Log stream prefix: `ecs`

**Health Check:**
- Command: `CMD-SHELL,curl -f http://localhost:5000/health || exit 1`
- Interval: 30 seconds
- Timeout: 5 seconds
- Start period: 60 seconds
- Retries: 3

**CLI Method (if you have the JSON file):**
```bash
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json --region ap-southeast-2
```

### Step 6: Create ECS Service

**AWS Console Method:**
1. Go to ECS Console → Clusters → radio-sahoo-cluster
2. Click "Create Service"
3. Launch type: Fargate
4. Task Definition: `radio-sahoo-task:1`
5. Service name: `radio-sahoo-service`
6. Number of tasks: 1

**Networking:**
- VPC: `vpc-21332c46`
- Subnets: Select all 3 subnets (`subnet-255aab6d`, `subnet-59dd1a3f`, `subnet-5391e70b`)
- Security Group: `sg-ffe07db6`
- Auto-assign public IP: ENABLED

**CLI Method:**
```bash
aws ecs create-service \
  --cluster radio-sahoo-cluster \
  --service-name radio-sahoo-service \
  --task-definition radio-sahoo-task:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-255aab6d,subnet-59dd1a3f,subnet-5391e70b],securityGroups=[sg-ffe07db6],assignPublicIp=ENABLED}" \
  --region ap-southeast-2
```

### Step 7: Find Your Application URL

**AWS Console Method:**
1. Go to ECS Console → Clusters → radio-sahoo-cluster
2. Click on `radio-sahoo-service`
3. Go to "Tasks" tab
4. Click on the running task
5. In "Network" section, copy the "Public IP"

**Access your app at:** `http://[PUBLIC_IP]:5000/radio`

**CLI Method:**
```bash
# Get task ARN
TASK_ARN=$(aws ecs list-tasks --cluster radio-sahoo-cluster --service-name radio-sahoo-service --query 'taskArns[0]' --output text --region ap-southeast-2)

# Get task details including public IP
aws ecs describe-tasks --cluster radio-sahoo-cluster --tasks $TASK_ARN --region ap-southeast-2 --query 'tasks[0].attachments[0].details[?name==`networkInterfaceId`].value' --output text
```

## 🔍 Monitoring & Troubleshooting

### Check Service Status
```bash
aws ecs describe-services --cluster radio-sahoo-cluster --services radio-sahoo-service --region ap-southeast-2
```

### View Logs
1. CloudWatch Console → Log groups → `/ecs/radio-sahoo`
2. Check the latest log stream for application logs

### Common Issues
1. **Task keeps stopping:** Check CloudWatch logs for errors
2. **Cannot access app:** Verify security group allows port 5000
3. **Image pull errors:** Ensure ECR repository has the image
4. **Health check failures:** Check if `/health` endpoint responds

## 🎯 Success Verification

Your deployment is successful when:
- [x] ECS service shows "RUNNING" status
- [x] Task health check passes
- [x] Application accessible at `http://[PUBLIC_IP]:5000/radio`
- [x] Radio stream plays correctly
- [x] Rating system works

## 📱 Next Steps (Optional)

1. **Set up Application Load Balancer** for better reliability
2. **Configure custom domain** with Route 53
3. **Add SSL certificate** with AWS Certificate Manager
4. **Set up auto-scaling** based on CPU/memory usage
5. **Configure CloudWatch alarms** for monitoring

---

**Radio Sahoo Manual Deployment Guide**  
*Version 1.0 - July 2025*

🎵 Deploy your music streaming platform to the cloud! 🎵