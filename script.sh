#!/bin/bash

#clone project
git clone https://github.com/14790897/Nighttime-Wisdom-Star.git /home/ubuntu/myapp

# 安装需求
pip install -r requirements.txt

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
