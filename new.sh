#!/bin/bash
mv .env.template .env


# 从.env文件中提取license_id
LICENSE_ID=$(grep 'LICENSE_ID' .env | cut -d "'" -f 2)

# Debug: Print extracted LICENSE_ID
echo "Extracted LICENSE_ID: $LICENSE_ID"

# 检查LICENSE_ID是否被成功提取
if [ -z "$LICENSE_ID" ]; then
    echo "License ID not found in .env file."
    exit 1
fi

# 使用新的license_id替换config.json中的license_id
sed -i "s/\"license_id\": \".*\"/\"license_id\": \"$LICENSE_ID\"/" data/config.json

echo "License ID updated in config.json."


