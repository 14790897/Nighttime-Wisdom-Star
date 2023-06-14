# [Nighttime-Wisdom-Star](https://github.com/14790897/Nighttime-Wisdom-Star)

[ENGLISH](README_EN.md)


## Project Overview

The purpose of this project is to create a platform that allows users who do not have direct access to GPT-4 to experience the power of GPT-4 through the plus account holder's share.

Demo address: [Registration and Login System --- Registration and Login System](https://share.liuweiqing.top/) (This is really gpt4) Sometimes it is not accessible because I may debug it.

tg exchange group: https://t.me/+tkxAZJNrwIpjYTk1

If there is a need, I will put out a video to explain the code in detail.

Interface display:

! [preview](/asset/preview.jpg)

## How it works

The free usage limit for GPT-4 is limited to a maximum of 25 requests every three hours. Since account holders need to rest at night, there are about 75 credits that cannot be used, so we can collect user questions during the day and then process them at night using the GPT-4 credits that are idle for plus account holders. User submitted questions will be temporarily stored in the Redis database with the key name "{username}:data". Processes in the project will listen to the time and when it reaches 0:00 am, start the processors, read the user-submitted questions, process them and store the results in the Redis database along with the original questions, with the key name "f"{username}:results". This data will be stored for a long time so that users can see the history of their conversations with GPT-4 when they visit the homepage later.

How does this project interact with the web version of ChatGPT? Actually, it uses [pengzhile/pandora: Pandora, a ChatGPT that helps you breathe smoothly. (github.com)](https://github.com/ pengzhile/pandora)

## How to use it (new version, convenient)

Welcome to the Nighttime Wisdom Star app. Here are the steps on how to install and run this app on your vps.

### Run Nighttime Wisdom Star

1. Enter the sudo mode of your vps

2. Ubuntu download the install_docker_and_compose_ubuntu.sh file.

   Command:

   ```bash
   wget https://raw.githubusercontent.com/14790897/Nighttime-Wisdom-Star/new-branch/install_docker_and_compose_ubuntu.sh
   ```

   centos download install_docker_and_compose_centos.sh file

   Command:

   ```bash
   wget https://raw.githubusercontent.com/14790897/Nighttime-Wisdom-Star/new-branch/install_docker_and_compose_centos.sh
   ```

3. Run the following command:

   ubuntu.

   ```bash
   . install_docker_and_compose_ubuntu.sh
   ```

   centos.

   ```bash
   . install_docker_and_compose_centos.sh
   ```

   You will be prompted to enter the appropriate environment variables, so follow the prompts.

4. Wait for Docker Compose to pull the required images and start the services, this may take some time depending on your network speed and machine performance.

5. Once all services are started, you can access [http://vps的IP:2345](http://vps的IP:2345) to use the Nighttime Wisdom Star application via your browser.

   ### Congratulations, great job!

   Next, you can configure nginx as required, either using domain access (which is not taught in this tutorial) or IP:port (port is 5000) for direct access.

## FQA

1. If you want to see all the data of registered users?

   Run the following command:

   ```bash
   docker-compose exec redis sh
   ```

   Enter ``redis-cli``, enter the database, and then please ask ChatGPT how to view the data of redis.

2. how to modify the runtime, total answer count, etc. again?

   Modify the corresponding values in the .env file, and run the following command to update it when you are done:

   ```bash
   docker-compose down
   ```

   ```bash
   docker-compose up -d
   ```

   If you encounter any problems with it, or have any suggestions, feel free to raise an issue.

### Thanks!