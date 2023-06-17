# [Nighttime-Wisdom-Star](https://github.com/14790897/Nighttime-Wisdom-Star)

[ENGLISH](README_EN.md)


## 项目概述

本项目旨在创建一个平台，让无法直接使用 GPT-4 的用户能够通过plus账号持有者的共享体验到 GPT-4 的强大功能。

演示地址：[Registration and Login System --- 注册和登录系统](https://share.liuweiqing.top/)(这是真的gpt4)由于我可能会调试，所以有时无法访问。

tg交流群：https://t.me/+tkxAZJNrwIpjYTk1

如果有需要的话，我会出一期视频详细讲解代码。

界面展示：

![preview](/asset/preview.jpg)

## 工作原理

GPT-4 的免费使用额度限制为每三小时最多25条请求。由于账号持有者晚上需要休息，有大约75条的额度无法使用，因此我们可以在白天收集用户的问题，然后在晚上利用plus账号持有者闲置的GPT-4额度进行处理。用户提交的问题将被暂存到Redis数据库中，键名为"{username}:data"。项目中的进程会监听时间，当到达凌晨0点后，启动处理程序，读取用户提交的问题，处理后将结果连同原始问题一起存入Redis数据库，键名为"f"{username}:results"。这些数据将被长期保存，以便用户在后续访问主页时能看到与GPT-4的历史对话记录。

本项目如何与网页版ChatGPT进行交互？其实是用了[pengzhile/pandora: 潘多拉，一个让你呼吸顺畅的ChatGPT。Pandora, a ChatGPT that helps you breathe smoothly. (github.com)](https://github.com/pengzhile/pandora)

## 使用方法（新版，方便）

欢迎使用 Nighttime Wisdom Star 应用。以下是如何在您的vps上安装和运行本应用的步骤。

### 运行 Nighttime Wisdom Star

1. 进入vps的sudo模式

2. Ubuntu下载并运行install_docker_and_compose_ubuntu.sh文件，

   指令：

   ```bash
   wget -O - https://raw.githubusercontent.com/14790897/Nighttime-Wisdom-Star/new-branch/install_docker_and_compose_ubuntu.sh | bash
   ```

   centos下载install_docker_and_compose_centos.sh文件

   指令：

   ```bash
   wget -O - https://raw.githubusercontent.com/14790897/Nighttime-Wisdom-Star/new-branch/install_docker_and_compose_centos.sh | bash
   ```
   系统会提示你输入相应环境变量，请按照提示操作。

3. 等待 Docker Compose 拉取所需的镜像并启动服务，这可能需要一些时间，具体取决于你的网络速度和机器性能。

4. 当所有服务都启动后，你就可以通过浏览器访问 [http://vps的IP:2345](http://vps的IP:2345) 来使用 Nighttime Wisdom Star 应用了。

   ### 恭喜你，大功告成

   接下来可以根据需求，进行nginx配置，可以使用域名访问（本教程就不教了），也可以IP:端口（端口是5000）直接访问。

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







