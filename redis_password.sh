#!/bin/bash

# 检查参数数量
if [ "$#" -ne 2 ]; then
    echo "用法: $0 <redis.conf的路径> <新密码>"
    exit 1
fi

CONF_FILE=$1
NEW_PASS=$2

# 检查 Redis 配置文件是否存在
if [ ! -f "$CONF_FILE" ]; then
    echo "配置文件不存在: $CONF_FILE"
    exit 1
fi

# 用新密码更新 requirepass 指令
if grep -q "^requirepass " "$CONF_FILE"; then
    # 如果文件中已有 requirepass 指令，就替换它
    sed -i "s/^requirepass .*/requirepass $NEW_PASS/" "$CONF_FILE"
else
    # 如果没有，就添加这个指令
    echo "requirepass $NEW_PASS" >> "$CONF_FILE"
fi

echo "Redis 密码已更新在配置文件: $CONF_FILE"