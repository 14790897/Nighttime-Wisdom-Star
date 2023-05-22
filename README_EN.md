# [Nighttime-Wisdom-Star](https://github.com/14790897/Nighttime-Wisdom-Star/tree/main)

[CHINESE](README.md)


## Project Overview

The purpose of this project is to create a platform that allows users who do not have direct access to GPT-4 to experience the power of GPT-4 through the plus account holder's share.

Demo address: [Registration and Login System --- Registration and Login System](http://35.166.94.139:5001/) Since I may debug, so sometimes I can't access, demo can be seen in [Personal Production -plus users share GPT4 usage times method to others_beep_ bilibili](https://www.bilibili.com/video/BV1kk4y1s7Ke/?spm_id_from=333.1007.top_right_bar_window_history.content.click&vd_source= 4a82a11c5d10f93386761e52d7c21d95)

If there is a need, I will make a video issue to explain the code in detail.

## How it works

The free usage limit of GPT-4 is limited to a maximum of 25 requests every three hours. Since account holders need to rest at night, there are about 75 credits that cannot be used, so we can collect users' questions during the day and then process them at night using the GPT-4 credits that are idle for plus account holders. User submitted questions will be temporarily stored in the Redis database with the key name "{username}:data". Processes in the project will listen to the time and when it reaches 0:00 am, start the processors, read the user-submitted questions, process them and store the results in the Redis database along with the original questions, with the key name "f"{username}:results". This data will be stored for a long time so that users can see the history of their conversations with GPT-4 when they visit the homepage later.

How does this project interact with the web version of ChatGPT? Actually, it uses [pengzhile/pandora: Pandora, a ChatGPT that helps you breathe smoothly. (github.com)](https://github.com/ pengzhile/pandora)

## How to use it (new version, convenient)

Welcome to the Nighttime Wisdom Star app. Here are the steps on how to install and run this app on your vps.

### Pre-requisites

To use this application, you need to install Docker and Docker Compose on your machine first. here is the installation guide on Ubuntu system, please refer to the official documentation for other operating systems. (If you already have Docker and Docker Compose installed, please skip this section)

#### Installing Docker.

1. Update your existing list package with:

```bash
sudo apt-get update
```

2. Install Docker's dependencies: ``bash

```bash
sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```bash

3. Add the official Docker GPG key: ``bash

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

4. Add the Docker repository:

```bash
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

5. Update the list of repositories:

```bash
sudo apt-get update
```

6. Install Docker CE:

``bash
sudo apt-get install docker-ce
```

Verify that the installation was successful:

```bash
sudo docker run hello-world
```

#### Install Docker Compose.

1. Download the current stable version of Docker Compose: ``bash

```bash
sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker -compose
```

2. Set executable permissions:

```bash
sudo chmod +x /usr/local/bin/docker-compose
```

Verify that the installation was successful: ``bash

```bash
docker-compose --version
```

### Run Nighttime Wisdom Star

1. Download the [docker-compose.yml](https://github.com/14790897/Nighttime-Wisdom-Star/blob/main/docker-compose.yml) file
2. Download the [.env.template]([Nighttime-Wisdom-Star/.env.template at main - 14790897/Nighttime-Wisdom-Star - GitHub](https://github.com/14790897/ Nighttime-Wisdom-Star/blob/main/.env.template), rename it to .env, and modify PANDORA_ACCESS_TOKEN to hold the accessToken obtained from https://chat.openai.com/api/auth/session. This is the key to interact with ChatGPT web side. 3.
3. Go to the directory where the `docker-compose.yml` file is located. 4.
4. Run the following command:

```bash
docker-compose up
```

Or add -d and run it in the background

```bash
docker-compose up -d
```

4. Wait for Docker Compose to pull the required images and start the services, this may take some time depending on your network speed and machine performance.

5. Once all services are started, you can access [http://vps的IP:5001](http://vps的IP:5001) to use the Nighttime Wisdom Star application via your browser.

6. If you want to view all the data of registered users?

   First use the background run mode, then run the following command

   ```
   docker-compose exec redis sh
   ```

   Enter ``redis-cli``, enter the database, and then please ask ChatGPT how to view the data of redis.

7. how to modify the runtime, total answer count?

   First clone the whole repository to your vps, in the vps repository directory, modify the corresponding part of pogress_in_back.py, save it and exit, then run `docker-compose build --build-arg CACHEBUST=$(date +%s) web`, rebuild the image, after that you can It's running, run the code: `docker-compose up -d`.

If you encounter any problems during use, or have any suggestions, feel free to raise an issue.

Thanks!

## Usage (old, complicated, not recommended, for users who don't know how to use docker, but it's not perfect yet) 

modify .env.template to .env and fill in the corresponding parameters, SECRET_KEY can be generated at will, URL for their own server Pandora project domain name, or will not configure the domain name, with the running Pandora project IP:port replacement can also be.

### Simplifying steps (this script is not yet complete):

```
chmod +x script.sh
. /script.sh
```

### Specific steps:

#### Install my project

Assuming your vps is an Ubuntu system.

In the /home/ubuntu directory (feel free to use the directory, but be careful to work in the same directory), download my GitHub project

```
git clone https://github.com/14790897/Nighttime-Wisdom-Star.git
```

Change `host=redis_host` (use the search function to find this line) to `host='localhost'` in app.py

```
sudo -i
```

Enter the following command

```
pip install -r requirements.txt
```

```
vim /etc/systemd/system/myapp.service
```

Press i to enter insert mode, copy the following, ctrl+shift+v to paste it, so that the project can run in the background

```
[Unit]
Description=My Python App
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/app
ExecStart=/usr/local/bin/gunicorn --bind 0.0.0.0:5000 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Press esc, enter :wq, save and exit the editor

Start running the command

```
systemctl start myapp
```

At the command line, enter the following command to make it boot up

```
systemctl enable myapp
```

#### Install Pandora

Download the Pandora project

```
git clone https://github.com/pengzhile/pandora.git
```

Then make the project run in the background

```
vim /etc/systemd/system/pandora.service
```

As before, copy the following into it

```
[Unit]
Description=Pandora Service
After=network.target

[Service]
ExecStart=/usr/local/bin/pandora -t t.json -s 0.0.0.0:8008
Restart=always
# need to replace with actual path
WorkingDirectory=/home/ubuntu

[Install]
WantedBy=multi-user.target
```

Start running the command

```
systemctl start myapp
```

Boot command

```
systemctl enable myapp
```

Create the t.json file in the /home/ubuntu directory and enter https://chat.openai.com/api/auth/session破解得到的账号access token.

#### Install the redis database.

Omit...

### Congratulations, great job!

Next you can configure nginx according to your needs, either using domain access (which is not taught in this tutorial) or IP:port (port is 5000) for direct access.