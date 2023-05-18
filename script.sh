#!/bin/bash

echo "Nighttime-Wisdom-Star"

# 更新软件包列表
sudo apt-get update

# 安装Redis
sudo apt-get install -y redis-server

# 备份Redis的默认配置文件（如果存在）
if [ -f /etc/redis/redis.conf ]; then
    sudo cp /etc/redis/redis.conf /etc/redis/redis.conf.bak
fi

# 写入新的配置
echo "save 900 1" | sudo tee -a /etc/redis/redis.conf
echo "save 300 10" | sudo tee -a /etc/redis/redis.conf
echo "save 60 10000" | sudo tee -a /etc/redis/redis.conf
echo "stop-writes-on-bgsave-error no" | sudo tee -a /etc/redis/redis.conf

# 重启Redis服务以应用新的配置
sudo systemctl restart redis.service

# make a directory
mkdir /home/ubuntu
mkdir /home/ubuntu/app

#clone project
git clone https://github.com/14790897/Nighttime-Wisdom-Star.git /home/ubuntu/myapp

#change directory and install requirements
(cd /home/ubuntu/myapp && pip install -r requirements.txt)

# 创建和写入 myapp.service 文件
echo "[Unit]
Description=My Python App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/app
ExecStart=/usr/local/bin/gunicorn --bind 127.0.0.1:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/myapp.service

# 启动服务
sudo systemctl start myapp

# 开启开机自启动
sudo systemctl enable myapp

#download pandora
pip install pandora-cloud

# 创建和写入 pandora.service 文件
echo "[Unit]
Description=Pandora Service
After=network.target

[Service]
ExecStart=/usr/local/bin/pandora -t t.json -s 127.0.0.1:8008
Restart=always
WorkingDirectory=/home/ubuntu

[Install]
WantedBy=multi-user.target
" | sudo tee /etc/systemd/system/pandora.service

# 启动服务
sudo systemctl start pandora

# 开启开机自启动
sudo systemctl enable pandora

# modify the .env file
# Check if .env file exists
if [ -f "/home/ubuntu/myapp/.env" ]; then
    # Backup .env file
    cp /home/ubuntu/myapp/.env /home/ubuntu/myapp/.env.bak

    # Use sed to replace the value of URL in .env file
    sed -i "s#URL=[^n]*#URL='127.0.0.1:8008'#g" /home/ubuntu/myapp/.env
    sed -i "s#SECRET_KEY=[^n]*#SECRET_KEY='477d75c5af744b76607fe86xcf8a5a368519acb486d62c5fa69bd42c16809f88'#g" /home/ubuntu/myapp/.env
else
    echo ".env file does not exist in the specified directory."
fi
