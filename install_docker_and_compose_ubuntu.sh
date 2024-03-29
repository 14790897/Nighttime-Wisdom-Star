#!/bin/bash

# 检查 Docker 是否已安装
if ! command -v docker &> /dev/null
then
    echo "Docker 未安装，开始安装 Docker..."

    # 卸载旧版本 Docker
    sudo apt-get remove -y docker docker-engine docker.io containerd runc

    # 更新 apt 包索引
    sudo apt-get update -y

    # 安装依赖以使 APT 可以通过 HTTPS 获取包
    sudo apt-get install -y \
        apt-transport-https \
        ca-certificates \
        curl \
        gnupg \
        lsb-release

    # 添加 Docker 的官方 GPG 密钥
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

    # 设置稳定版仓库
    echo \
    "deb [arch=amd64 signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
    $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

    # 更新 apt 包索引，然后安装最新版本的 Docker Engine 和 containerd
    sudo apt-get update -y
    sudo apt-get install -y docker-ce docker-ce-cli containerd.io

    echo "Docker 已成功安装！"
else
    echo "Docker 已安装，跳过..."
fi

# 检查 Docker Compose 是否已安装
if ! command -v docker-compose &> /dev/null
then
    echo "Docker Compose 未安装，开始安装 Docker Compose..."

    # 安装 Docker Compose
    sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose

    echo "Docker Compose 已成功安装！"
else
    echo "Docker Compose 已安装，跳过..."
fi

# URL of the files to be downloaded
url1='https://raw.githubusercontent.com/14790897/Nighttime-Wisdom-Star/new-branch/docker-compose.yml'
url2='https://raw.githubusercontent.com/14790897/Nighttime-Wisdom-Star/new-branch/.env.template'

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
sed -i "s|ENV=.*|ENV=$ENV|g" .env

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
sed -i "s#time_zone=.*#time_zone=$time_zone#g" .env

echo "Environment variables set successfully!"

sudo docker-compose up -d
