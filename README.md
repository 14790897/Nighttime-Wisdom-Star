# [Nighttime-Wisdom-Star](https://github.com/14790897/Nighttime-Wisdom-Star)

[ENGLISH](README_EN.md)


## 项目概述

本项目旨在创建一个平台，让无法直接使用 GPT-4 的用户能够通过plus账号持有者的共享体验到 GPT-4 的强大功能。

# 目前已经取消订阅Plus，我使用perplexity的免费gpt4，好像有方法也可以转换它的API但是我目前还没有学会，所以下面的演示站只有3.5
演示地址：https://share.liuweiqing.top/(可以看网页上面的允许使用时间来确定当前是否能立即负责响应)

tg交流群：https://t.me/+tkxAZJNrwIpjYTk1

界面展示：

![preview](/asset/preview.jpg)

## 工作原理

GPT-4 的免费使用额度限制为每三小时最多40条请求。由于账号持有者晚上需要休息，有大约40*3条的额度无法使用，因此我们可以在白天收集用户的问题，然后在晚上利用plus账号持有者闲置的GPT-4额度进行处理。用户提交的问题将被暂存到Redis数据库中，键名为"{username}:data"。项目中的进程会监听时间，当到达凌晨0点后，启动处理程序，读取用户提交的问题，处理后将结果连同原始问题一起存入Redis数据库，键名为"f"{username}:results"。这些数据将被长期保存，以便用户在后续访问主页时能看到与GPT-4的历史对话记录。

本项目如何与网页版ChatGPT进行交互？其实是用了[pandora-next](https://github.com/pandora-next/deploy)

## 使用方法

1. 按照.env.template注释的要求更改文件
2. 运行目录下的new.sh脚本, 代码：`source new.sh`
3. 运行 `bash redis_password.sh redis.conf` 设置redis的密码，这个不做的话，别人就可以清空你的数据库
4. 目录下运行 `docker-compose up -d` 

## FQA

1. 如果想查看注册用户的所有数据？

   运行以下命令：

   ```bash
   docker-compose exec redis bash
   ```

   输入`redis-cli`，进入数据库，然后请请教ChatGPT如何查看redis的数据。

2. 如何再次修改运行时间，总回答次数等环境变量？

   直接修改.env文件中对应的值，完成后运行以下命令更新：

   ```bash
   docker-compose down
   ```

   ```bash
   docker-compose up -d
   ```
3. 隐藏的自动化功能，只要在redis中任意创建一个键'用户名:data'，将你想要提问的问题放入此键对应的列表，程序就能识别了

   如果你在使用过程中遇到任何问题，或者有任何建议，欢迎提issue。

### 谢谢！







