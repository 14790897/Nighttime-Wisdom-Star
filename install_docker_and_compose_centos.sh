#!/bin/bash

# 卸载旧版本Docker
sudo yum remove -y docker docker-client docker-client-latest docker-common docker-latest docker-latest-logrotate docker-logrotate docker-engine

# 安装依赖工具
sudo yum install -y yum-utils

# 设置Docker仓库
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo

# 安装 Docker
sudo yum install -y docker-ce docker-ce-cli containerd.io

# 启动 Docker
sudo systemctl start docker

# Docker开机启动
sudo systemctl enable docker

# 安装 docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Docker and Docker Compose installed successfully!"

# URL of the files to be downloaded
url1='https://github.com/14790897/Nighttime-Wisdom-Star/raw/main/docker-compose.yml'
url2='https://github.com/14790897/Nighttime-Wisdom-Star/raw/main/.env.template'

# Install wget
sudo yum install -y wget

# Download the files using wget
wget $url1
wget $url2

# Rename .env.template to .env
mv .env.template .env

# Default values from existing .env file
PANDORA_ACCESS_TOKEN_OLD=$(grep 'PANDORA_ACCESS_TOKEN' .env | cut -d '=' -f2)
start_time_old=$(grep 'start_time' .env | cut -d '=' -f2)
end_time_old=$(grep 'end_time' .env | cut -d '=' -f2)
amount_old=$(grep 'amount' .env | cut -d '=' -f2)
time_zone_old=$(grep 'time_zone' .env | cut -d '=' -f2)

# Request user input
echo "Please provide the following information (or press enter to keep current value):"

# Access Token
echo "PANDORA_ACCESS_TOKEN (Get it from: https://chat.openai.com/api/auth/session):"
read PANDORA_ACCESS_TOKEN
if [ -z "$PANDORA_ACCESS_TOKEN" ]; then
  PANDORA_ACCESS_TOKEN=$PANDORA_ACCESS_TOKEN_OLD
fi
sed -i "s|PANDORA_ACCESS_TOKEN=.*|PANDORA_ACCESS_TOKEN='$PANDORA_ACCESS_TOKEN'|g" .env

# Processing Time
echo "Start time for processing events (0-24):"
read start_time
if [ -z "$start_time" ]; then
  start_time=$start_time_old
fi
sed -i "s|start_time=.*|start_time=$start_time|g" .env

echo "End time for processing events (0-24):"
read end_time
if [ -z "$end_time" ]; then
  end_time=$end_time_old
fi
sed -i "s|end_time=.*|end_time=$end_time|g" .env

# Number of Issues Processed Daily
echo "Number of issues processed daily:"
read amount
if [ -z "$amount" ]; then
  amount=$amount_old
fi
sed -i "s|amount=.*|amount=$amount|g" .env

# Time Zone
echo "Time Zone (Example: Asia/Shanghai):"
read time_zone
if [ -z "$time_zone" ]; then
  time_zone=$time_zone_old
fi
sed -i "s|time_zone=.*|time_zone='$time_zone'|g" .env

echo "Environment variables set successfully!"

# Start up docker-compose
sudo docker-compose up -d
