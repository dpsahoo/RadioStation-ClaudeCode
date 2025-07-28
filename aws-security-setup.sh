#!/bin/bash
# Security Group Setup for Radio Sahoo

set -e

AWS_REGION="ap-southeast-2"
SECURITY_GROUP_ID="sg-ffe07db6"

echo "🔒 Setting up Security Group Rules for Radio Sahoo"
echo "================================================="

# Allow HTTP traffic on port 5000 (Flask app)
echo "📝 Adding rule for HTTP traffic on port 5000..."
aws ec2 authorize-security-group-ingress \
  --group-id ${SECURITY_GROUP_ID} \
  --protocol tcp \
  --port 5000 \
  --cidr 0.0.0.0/0 \
  --region ${AWS_REGION} 2>/dev/null || echo "Rule may already exist"

# Allow HTTP traffic on port 80 (for ALB)
echo "📝 Adding rule for HTTP traffic on port 80..."
aws ec2 authorize-security-group-ingress \
  --group-id ${SECURITY_GROUP_ID} \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0 \
  --region ${AWS_REGION} 2>/dev/null || echo "Rule may already exist"

# Allow HTTPS traffic on port 443 (for future SSL)
echo "📝 Adding rule for HTTPS traffic on port 443..."
aws ec2 authorize-security-group-ingress \
  --group-id ${SECURITY_GROUP_ID} \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0 \
  --region ${AWS_REGION} 2>/dev/null || echo "Rule may already exist"

echo "✅ Security group rules configured!"
echo "🔍 Current security group rules:"
aws ec2 describe-security-groups --group-ids ${SECURITY_GROUP_ID} --region ${AWS_REGION} --output table