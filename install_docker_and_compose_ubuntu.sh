#!/bin/bash

# 卸载旧版本Docker
sudo apt-get remove -y docker docker-engine docker.io containerd runc

# 更新apt包索引
sudo apt-get update -y

# 安装依赖以使APT可以通过HTTPS来获取包
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# 添加Docker的官方GPG密钥
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 设置稳定版仓库
echo \
  "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 更新apt包索引，然后安装最新版本的Docker Engine和containerd
sudo apt-get update -y
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 安装docker-compose
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

echo "Docker and Docker Compose installed successfully!"

# URL of the files to be downloaded
url1='https://github.com/14790897/Nighttime-Wisdom-Star/raw/main/docker-compose.yml'
url2='https://github.com/14790897/Nighttime-Wisdom-Star/raw/main/.env.template'

# Download the files using wget or curl

# Using wget
sudo apt install -y curl wget
wget $url1
wget $url2

# Or using curl
# curl -O $url1
# curl -O $url2

sudo mv .env.template .env

# Default values from existing .env file
PANDORA_ACCESS_TOKEN_OLD=$(grep 'PANDORA_ACCESS_TOKEN' .env | cut -d '=' -f2)
start_time_old=$(grep 'start_time' .env | cut -d '=' -f2)
end_time_old=$(grep 'end_time' .env | cut -d '=' -f2)
amount_old=$(grep 'amount' .env | cut -d '=' -f2)
time_zone_old=$(grep 'time_zone' .env | cut -d '=' -f2)
ENV_old=$(grep 'ENV' .env | cut -d '=' -f2)

# Request user input
echo "Please provide the following information (or press enter to keep current value):"

#env
echo "Environment setting (default: 'production', change this to 'development' to get immediate answers):"
read ENV
if [ -z "$ENV" ]; then
  ENV=$ENV_old
fi
sed -i "s|ENV=.*|ENV='$ENV'|g" .env

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
echo "Time Zone (Example: Asia/Shanghai)(check:sudo timedatectl list-timezones):"
read time_zone
if [ -z "$time_zone" ]; then
  time_zone=$time_zone_old
fi
sed -i "s#time_zone=.*#time_zone='$time_zone'#g" .env

echo "Environment variables set successfully!"

sudo docker-compose up -d
