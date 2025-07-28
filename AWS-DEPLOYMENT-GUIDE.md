# 🚀 AWS Docker Deployment Guide: Radio Sahoo Journey

*A comprehensive guide to deploying a Dockerized Flask application on AWS ECS Fargate*

---

## 📖 Table of Contents

1. [Overview](#overview)
2. [Why AWS for Docker Deployment?](#why-aws-for-docker-deployment)
3. [AWS Services Used](#aws-services-used)
4. [Architecture Diagram](#architecture-diagram)
5. [Step-by-Step Deployment Process](#step-by-step-deployment-process)
6. [IAM Roles and Security](#iam-roles-and-security)
7. [Networking Configuration](#networking-configuration)
8. [Docker Platform Considerations](#docker-platform-considerations)
9. [Monitoring and Logging](#monitoring-and-logging)
10. [Cost Breakdown](#cost-breakdown)
11. [Troubleshooting Common Issues](#troubleshooting-common-issues)
12. [Next Steps and Improvements](#next-steps-and-improvements)

---

## 🎯 Overview

This guide documents the complete journey of deploying **Radio Sahoo**, a Flask-based HLS radio streaming application, from a local Docker container to a production-ready AWS cloud deployment.

### **What We Accomplished:**
- 🐳 Containerized a Flask application with Docker
- ☁️ Deployed to AWS ECS Fargate (serverless containers)
- 🔐 Implemented proper security with IAM roles
- 🌐 Made the application publicly accessible
- 📊 Set up monitoring and logging
- 💰 Achieved cost-effective hosting (~$10-15/month)

---

## 🤔 Why AWS for Docker Deployment?

### **Traditional Hosting vs. AWS Container Services**

| Aspect | Traditional VPS | AWS ECS Fargate |
|--------|----------------|-----------------|
| **Server Management** | Manual OS updates, patches | Fully managed |
| **Scaling** | Manual resize/migrate | Auto-scaling |
| **Availability** | Single point of failure | Multi-AZ deployment |
| **Security** | Self-managed | AWS security baseline |
| **Cost** | Fixed monthly fee | Pay per actual usage |
| **Deployment** | SSH + manual commands | Infrastructure as Code |

### **Why ECS Fargate Specifically?**
- **Serverless Containers:** No EC2 instances to manage
- **Auto-scaling:** Handles traffic spikes automatically  
- **Security:** AWS handles underlying infrastructure security
- **Integration:** Seamless with other AWS services
- **Cost-effective:** Pay only for resources used

---

## 🛠️ AWS Services Used

### **Core Container Services**

#### **1. Amazon ECR (Elastic Container Registry)**
- **Purpose:** Docker image storage and management
- **Why Used:** Secure, private registry for our Radio Sahoo Docker images
- **Alternative:** Docker Hub (public, less secure for private apps)

**What it does:**
```bash
# Store Docker images securely
docker push 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo:amd64
```

#### **2. Amazon ECS (Elastic Container Service)**
- **Purpose:** Container orchestration and management
- **Why Used:** Manages container lifecycle, health checks, and deployments
- **Alternative:** Kubernetes (more complex), Docker Swarm (less features)

**Key Components:**
- **Clusters:** Logical grouping of compute resources
- **Task Definitions:** Blueprint for running containers
- **Services:** Maintains desired number of running tasks

#### **3. AWS Fargate**
- **Purpose:** Serverless compute engine for containers
- **Why Used:** No server management, automatic scaling, built-in security
- **Alternative:** EC2 launch type (requires managing instances)

**Benefits:**
- No EC2 instances to patch or maintain
- Automatic resource scaling
- Built-in networking and security

---

### **Supporting AWS Services**

#### **4. AWS VPC (Virtual Private Cloud)**
- **Purpose:** Isolated network environment
- **Why Used:** Security and network isolation for our application
- **Components Used:**
  - **Subnets:** Multiple availability zones for redundancy
  - **Security Groups:** Firewall rules for our application
  - **Internet Gateway:** Public internet access

#### **5. Amazon CloudWatch**
- **Purpose:** Monitoring, logging, and observability
- **Why Used:** Track application health, performance, and debugging
- **Features:**
  - **Log Groups:** Centralized application logs
  - **Health Checks:** Monitor container health
  - **Metrics:** CPU, memory, network usage

#### **6. AWS IAM (Identity and Access Management)**
- **Purpose:** Security and access control
- **Why Used:** Secure access between AWS services
- **Components:**
  - **Roles:** Define what services can do
  - **Policies:** Specific permissions
  - **Trust Relationships:** Who can assume roles

---

## 🏗️ Architecture Diagram

```
Internet Users
       ↓
   Public Internet
       ↓
 ┌─────────────────────────────────────┐
 │               AWS Cloud              │
 │                                     │
 │  ┌─────────────────────────────────┐ │
 │  │            VPC                  │ │
 │  │  ┌─────────────────────────────┐ │ │
 │  │  │      Security Group         │ │ │
 │  │  │   (Ports 80, 443, 5000)    │ │ │
 │  │  │                             │ │ │
 │  │  │  ┌─────────────────────────┐ │ │ │
 │  │  │  │    ECS Fargate Task     │ │ │ │
 │  │  │  │                         │ │ │ │
 │  │  │  │  ┌─────────────────────┐ │ │ │ │
 │  │  │  │  │  Radio Sahoo        │ │ │ │ │
 │  │  │  │  │  Docker Container   │ │ │ │ │
 │  │  │  │  │  (Port 5000)        │ │ │ │ │
 │  │  │  │  │                     │ │ │ │ │
 │  │  │  │  │  Flask App          │ │ │ │ │
 │  │  │  │  │  SQLite DB          │ │ │ │ │
 │  │  │  │  │  HLS Player         │ │ │ │ │
 │  │  │  │  └─────────────────────┘ │ │ │ │
 │  │  │  └─────────────────────────┘ │ │ │
 │  │  └─────────────────────────────┘ │ │
 │  └─────────────────────────────────┘ │
 └─────────────────────────────────────┘
          ↑                    ↑
    ┌─────────┐          ┌─────────────┐
    │   ECR   │          │ CloudWatch  │
    │(Images) │          │   (Logs)    │
    └─────────┘          └─────────────┘
```

---

## 📋 Step-by-Step Deployment Process

### **Phase 1: Preparation and Setup**

#### **Step 1: AWS CLI Configuration**
```bash
# Configure AWS credentials
aws configure list
```
- **Purpose:** Authenticate with AWS services
- **Required:** Access keys with appropriate permissions

#### **Step 2: Create ECR Repository**
```bash
# Create private Docker registry
Repository: radio-sahoo
URI: 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo
```
- **Why:** Secure storage for our Docker images
- **Alternative:** Public Docker Hub (less secure)

---

### **Phase 2: Container Preparation**

#### **Step 3: Build Docker Image for Correct Architecture**
```bash
# Critical: Build for AMD64 (not ARM64 from Mac)
docker build --platform linux/amd64 -f Dockerfile.simple -t radio-sahoo:amd64 .
```

**🚨 Important Platform Consideration:**
- **Apple Silicon Mac:** Builds ARM64 by default
- **AWS Fargate:** Runs on AMD64/x86_64 architecture
- **Solution:** Use `--platform linux/amd64` flag

#### **Step 4: Push Image to ECR**
```bash
# Login to ECR
aws ecr get-login-password --region ap-southeast-2 | docker login --username AWS --password-stdin 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com

# Tag and push
docker tag radio-sahoo:amd64 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo:amd64
docker push 896820529994.dkr.ecr.ap-southeast-2.amazonaws.com/radio-sahoo:amd64
```

---

### **Phase 3: AWS Infrastructure Setup**

#### **Step 5: Create IAM Roles**

**A. Task Execution Role (`RadioSahooTaskExecutionRole`)**
- **Purpose:** Allows ECS to manage your container
- **Permissions:**
  - Pull images from ECR
  - Create CloudWatch log streams
  - Manage container lifecycle

**B. Task Role (`RadioSahooTaskRole`)**
- **Purpose:** Allows your application to access AWS services
- **Permissions:** Basic logging (expandable for future features)

#### **Step 6: Create ECS Cluster**
```bash
aws ecs create-cluster --cluster-name radio-sahoo-cluster --region ap-southeast-2
```
- **Purpose:** Logical grouping for our container tasks
- **Type:** Fargate (serverless)

#### **Step 7: Register Task Definition**
```json
{
  "family": "radio-sahoo-task",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "256",
  "memory": "512",
  "executionRoleArn": "arn:aws:iam::896820529994:role/RadioSahooTaskExecutionRole",
  "taskRoleArn": "arn:aws:iam::896820529994:role/RadioSahooTaskRole",
  "containerDefinitions": [...]
}
```

**Why These Resources:**
- **CPU: 0.25 vCPU:** Sufficient for a Flask app with light load
- **Memory: 512 MB:** Adequate for Flask + SQLite + basic caching
- **Network Mode: awsvpc:** Each task gets its own network interface

---

### **Phase 4: Networking Configuration**

#### **Step 8: Configure VPC and Security Groups**

**VPC Configuration:**
- **VPC ID:** `vpc-21332c46` (default VPC)
- **Subnets:** Multiple AZs for redundancy
  - `subnet-255aab6d`
  - `subnet-59dd1a3f` 
  - `subnet-5391e70b`

**Security Group Rules:**
```bash
# Allow HTTP traffic on port 5000 (Flask app)
Port 5000: 0.0.0.0/0 (TCP)

# Allow HTTP traffic on port 80 (future load balancer)
Port 80: 0.0.0.0/0 (TCP)

# Allow HTTPS traffic on port 443 (future SSL)
Port 443: 0.0.0.0/0 (TCP)
```

---

### **Phase 5: Service Deployment**

#### **Step 9: Create ECS Service**
```bash
aws ecs create-service \
  --cluster radio-sahoo-cluster \
  --service-name radio-sahoo-service \
  --task-definition radio-sahoo-task:4 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[...],securityGroups=[...],assignPublicIp=ENABLED}"
```

**Service Configuration:**
- **Desired Count:** 1 (can auto-scale based on load)
- **Public IP:** Enabled (for direct internet access)
- **Health Checks:** Built-in container health monitoring

---

## 🔐 IAM Roles and Security

### **Understanding the Two-Role Pattern**

AWS ECS uses a **separation of concerns** security model:

#### **1. Task Execution Role (Infrastructure)**
```json
{
  "Role": "RadioSahooTaskExecutionRole",
  "Purpose": "ECS service management",
  "Permissions": [
    "ecr:GetAuthorizationToken",
    "ecr:BatchCheckLayerAvailability", 
    "ecr:GetDownloadUrlForLayer",
    "ecr:BatchGetImage",
    "logs:CreateLogStream",
    "logs:PutLogEvents"
  ]
}
```

**When it's used:**
- Container startup and shutdown
- Pulling Docker images from ECR
- Creating CloudWatch log streams
- Health check execution

#### **2. Task Role (Application)**
```json
{
  "Role": "RadioSahooTaskRole",
  "Purpose": "Application AWS access",
  "Permissions": [
    "logs:CreateLogGroup",
    "logs:PutLogEvents"
  ]
}
```

**When it's used:**
- While your application is running
- Making AWS API calls from within the container
- Accessing S3, DynamoDB, SES, etc. (if needed)

### **Security Best Practices Implemented**

1. **Principle of Least Privilege:** Each role has minimal required permissions
2. **Role Separation:** Infrastructure vs. application concerns
3. **No Hard-coded Credentials:** AWS handles authentication automatically
4. **Network Isolation:** VPC and security groups control access
5. **Private Registry:** ECR instead of public Docker Hub

---

## 🌐 Networking Configuration

### **VPC (Virtual Private Cloud) Basics**

**What is a VPC?**
A VPC is your own isolated section of the AWS cloud where you can launch resources in a network that you define.

**Our VPC Setup:**
```
VPC: vpc-21332c46 (Default VPC)
├── Subnet 1: subnet-255aab6d (AZ: ap-southeast-2a)
├── Subnet 2: subnet-59dd1a3f (AZ: ap-southeast-2b)  
└── Subnet 3: subnet-5391e70b (AZ: ap-southeast-2c)
```

### **Why Multiple Subnets?**
- **High Availability:** If one AZ fails, others continue running
- **Load Distribution:** Traffic can be spread across zones
- **Future Load Balancer:** Requires subnets in multiple AZs

### **Security Groups as Firewalls**

**Security Group: sg-ffe07db6**
```
Inbound Rules:
- Port 5000 (TCP): 0.0.0.0/0  # Flask application
- Port 80 (TCP): 0.0.0.0/0    # HTTP (future ALB)
- Port 443 (TCP): 0.0.0.0/0   # HTTPS (future SSL)

Outbound Rules:
- All traffic: 0.0.0.0/0       # Allow all outbound
```

### **Public IP Assignment**
- **Why Needed:** Direct internet access to our application
- **How:** `assignPublicIp=ENABLED` in network configuration
- **Result:** Each task gets a unique public IP address

---

## 🐳 Docker Platform Considerations

### **The ARM64 vs AMD64 Challenge**

This was the **critical issue** that initially prevented deployment:

#### **The Problem:**
```bash
# On Apple Silicon Mac (M1/M2)
docker build -t radio-sahoo .
# ↳ Creates ARM64 image by default

# AWS Fargate attempts to run
# ❌ Error: "image Manifest does not contain descriptor matching platform 'linux/amd64'"
```

#### **The Solution:**
```bash
# Explicitly build for AMD64
docker build --platform linux/amd64 -t radio-sahoo:amd64 .
# ↳ Creates AMD64 image compatible with AWS Fargate
```

#### **Why This Happens:**
- **Apple Silicon Macs:** Use ARM64 architecture
- **AWS Fargate:** Runs on Intel x86_64/AMD64 architecture
- **Docker Default:** Builds for host platform unless specified
- **Container Registries:** Store platform-specific images

#### **Best Practices:**
1. **Always specify platform** for production builds
2. **Test locally** with the same platform as production
3. **Use multi-platform builds** for broader compatibility

```bash
# Multi-platform build (advanced)
docker buildx build --platform linux/amd64,linux/arm64 -t radio-sahoo .
```

---

## 📊 Monitoring and Logging

### **CloudWatch Integration**

#### **Log Groups:**
```
Log Group: /ecs/radio-sahoo
├── Log Stream: ecs/radio-sahoo/task-id-1
├── Log Stream: ecs/radio-sahoo/task-id-2
└── ...
```

**What Gets Logged:**
- Application startup logs
- HTTP request logs
- Error messages and stack traces
- Database operations
- Health check results

#### **Health Checks:**
```json
{
  "healthCheck": {
    "command": ["CMD-SHELL", "curl -f http://localhost:5000/health || exit 1"],
    "interval": 30,
    "timeout": 5,
    "retries": 3,
    "startPeriod": 60
  }
}
```

**Health Check Flow:**
1. **Start Period:** 60 seconds for application warmup
2. **Regular Checks:** Every 30 seconds
3. **Failure Detection:** 3 consecutive failures triggers restart
4. **Endpoint:** `/health` returns application status

### **Monitoring Metrics:**

**Task-Level Metrics:**
- CPU utilization
- Memory utilization  
- Network I/O
- Task start/stop events

**Service-Level Metrics:**
- Running task count
- Pending task count
- Service events and deployments

---

## 💰 Cost Breakdown

### **Monthly Cost Estimate**

| Service | Resource | Cost |
|---------|----------|------|
| **ECS Fargate** | 0.25 vCPU | ~$7.20 |
| **ECS Fargate** | 0.5 GB Memory | ~$1.57 |
| **ECR Storage** | ~1 GB | ~$0.10 |
| **CloudWatch Logs** | ~1 GB/month | ~$0.50 |
| **Data Transfer** | First 1 GB free | $0.00 |
| **VPC/Networking** | Included | $0.00 |
| **Total** | | **~$9.37/month** |

### **Cost Optimization Tips:**

1. **Right-size Resources:** Monitor usage and adjust CPU/memory
2. **Log Retention:** Set CloudWatch log retention policies
3. **Reserved Capacity:** Consider Fargate Spot for development
4. **Data Transfer:** Use CloudFront CDN for static assets

### **Scaling Cost Impact:**

**If traffic increases 10x:**
- **Auto-scaling:** Up to 10 tasks (10x cost = ~$94/month)
- **Alternative:** Optimize code, use load balancer, CDN
- **Enterprise:** Consider EC2 instances with Reserved Instances

---

## 🔧 Troubleshooting Common Issues

### **1. Container Platform Mismatch**
```
Error: "image Manifest does not contain descriptor matching platform 'linux/amd64'"

Solution:
docker build --platform linux/amd64 -t myapp .
```

### **2. Task Keeps Stopping**
```
Symptoms: Tasks start but immediately stop

Common Causes:
- Application crashes on startup
- Health check failures
- Port configuration issues

Debugging:
1. Check CloudWatch logs: /ecs/radio-sahoo
2. Verify health check endpoint works
3. Test Docker image locally first
```

### **3. Cannot Access Application**
```
Symptoms: Task running but URL not accessible

Common Causes:
- Security group blocks traffic
- Wrong port configuration
- Public IP not assigned

Solutions:
1. Verify security group allows port 5000
2. Confirm assignPublicIp=ENABLED
3. Check task's public IP address
```

### **4. Image Pull Failures**
```
Error: "CannotPullContainerError"

Common Causes:
- ECR permissions missing
- Wrong image URI
- Image doesn't exist

Solutions:
1. Verify ECR permissions in task execution role
2. Check image exists: aws ecr describe-images
3. Confirm correct image URI in task definition
```

### **5. IAM Permission Errors**
```
Error: "User is not authorized to perform: ecs:CreateService"

Solutions:
1. Add AmazonECS_FullAccess policy
2. Create custom policy with specific permissions
3. Add iam:PassRole permission for task roles
```

---

## 🚀 Next Steps and Improvements

### **Immediate Enhancements**

#### **1. Add Application Load Balancer (ALB)**
- **Benefits:** SSL termination, custom domain, better availability
- **Cost:** ~$16/month additional
- **Implementation:**
```bash
aws elbv2 create-load-balancer \
  --name radio-sahoo-alb \
  --subnets subnet-255aab6d subnet-59dd1a3f \
  --security-groups sg-ffe07db6
```

#### **2. Custom Domain with Route 53**
- **Benefits:** Professional URL (radio.yourdomain.com)
- **Cost:** $0.50/month per hosted zone
- **SSL:** Free with AWS Certificate Manager

#### **3. Database Upgrade**
- **Current:** SQLite (file-based)
- **Upgrade:** Amazon RDS PostgreSQL
- **Benefits:** Better performance, backups, scaling
- **Cost:** ~$15/month for db.t3.micro

### **Production Readiness**

#### **1. Environment Configuration**
```bash
# Separate environments
- Development: radio-sahoo-dev
- Staging: radio-sahoo-staging  
- Production: radio-sahoo-prod
```

#### **2. Auto-scaling Policies**
```json
{
  "targetTrackingScalingPolicy": {
    "targetValue": 70.0,
    "scaleInCooldown": 300,
    "scaleOutCooldown": 60,
    "metric": "CPUUtilization"
  }
}
```

#### **3. Blue/Green Deployments**
- **CodeDeploy:** Zero-downtime deployments
- **Benefits:** Safe rollouts, instant rollbacks
- **Monitoring:** Real-time deployment health

#### **4. Enhanced Security**
```bash
# Additional security measures
- AWS WAF (Web Application Firewall)
- VPC Flow Logs
- AWS GuardDuty (threat detection)
- Secrets Manager (for sensitive config)
```

### **Advanced Features**

#### **1. Content Delivery Network (CDN)**
- **CloudFront:** Cache static assets globally
- **Benefits:** Faster load times, reduced server load
- **Cost:** Pay per usage (often reduces overall costs)

#### **2. Monitoring and Alerting**
```bash
# CloudWatch Alarms
- High CPU usage
- Memory utilization
- Error rate thresholds
- Custom application metrics
```

#### **3. CI/CD Pipeline**
```yaml
# GitHub Actions / AWS CodePipeline
1. Code commit → GitHub
2. Automated tests → Jest/Pytest
3. Build Docker image → ECR
4. Deploy to staging → ECS
5. Integration tests → Automated
6. Deploy to production → ECS
```

#### **4. Data Persistence**
- **Current:** Container storage (ephemeral)
- **Upgrade:** Amazon EFS (persistent file storage)
- **Database:** Amazon RDS with automated backups

---

## 📚 Key Learnings and Best Practices

### **Docker Best Practices**
1. **Multi-stage builds** for smaller images
2. **Platform specification** for cross-architecture compatibility
3. **Health checks** for container monitoring
4. **Non-root users** for security
5. **Environment variables** for configuration

### **AWS Best Practices**
1. **IAM least privilege** principle
2. **Multi-AZ deployment** for availability
3. **CloudWatch monitoring** for observability
4. **Security groups** as application firewalls
5. **Infrastructure as Code** for reproducibility

### **Cost Optimization**
1. **Right-size resources** based on actual usage
2. **Reserved capacity** for predictable workloads
3. **Spot instances** for development environments
4. **CloudWatch log retention** policies
5. **Regular cost review** and optimization

### **Security Fundamentals**
1. **No hardcoded secrets** in code or images
2. **Network isolation** with VPCs and security groups
3. **Regular updates** of base images and dependencies
4. **Audit logging** enabled
5. **Access reviews** and principle of least privilege

---

## 🎯 Conclusion

This deployment successfully demonstrates how to:

✅ **Containerize** a complex Flask application with HLS streaming  
✅ **Deploy** to AWS cloud infrastructure using modern best practices  
✅ **Secure** the application with proper IAM roles and network controls  
✅ **Monitor** application health and performance  
✅ **Scale** cost-effectively with serverless containers  

The **Radio Sahoo** application is now:
- 🌍 **Globally accessible** via public internet
- 🔒 **Secure** with AWS security baseline
- 📈 **Scalable** with auto-scaling capabilities
- 💰 **Cost-effective** at ~$10/month
- 🔧 **Maintainable** with Infrastructure as Code

This foundation provides an excellent starting point for building production-grade applications on AWS with modern containerization practices.

---

**Radio Sahoo AWS Deployment Guide**  
*Version 1.0 - July 2025*

🎵 **From localhost to the cloud - Your music streaming platform is now live!** 🎵

---

*For questions or improvements to this guide, please refer to the project documentation or create an issue in the repository.*