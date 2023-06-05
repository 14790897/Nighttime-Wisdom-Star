# [Nighttime-Wisdom-Star](https://github.com/14790897/Nighttime-Wisdom-Star/tree/main)

[ENGLISH](README_EN.md)


## Project Overview

This project aims to create a platform that allows users who cannot directly use GPT-4 to experience the powerful functions of GPT-4 through the sharing of plus account holders.

Demo address: [Registration and Login System --- Registration and Login System](http://35.166.94.139:5001/) Because I may be debugging, sometimes I cannot access it.

If necessary, I will release a video to explain the code in detail.

Interface display:

![preview](/asset/preview.jpg)

## working principle

The free usage quota for GPT-4 is limited to a maximum of 25 requests every three hours. Since account holders need to rest at night, there are about 75 quotas that cannot be used, so we can collect user questions during the day, and then use the idle GPT-4 quota of plus account holders to deal with them at night. Questions submitted by users will be temporarily stored in the Redis database with the key name "{username}:data". The process in the project will monitor the time. When it reaches 0 o'clock in the morning, start the processing program, read the questions submitted by the user, and store the results together with the original questions in the Redis database after processing. The key name is "f"{username}:results ". These data will be stored for a long time, so that users can see the historical conversation records with GPT-4 when they visit the homepage later.

How does this project interact with the web version of ChatGPT? In fact, I used [pengzhile/pandora: Pandora, a ChatGPT that allows you to breathe smoothly. Pandora, a ChatGPT that helps you breathe smoothly. (github.com)](https://github.com/pengzhile/pandora)

## How to use (new version, convenient)

Welcome to the Nighttime Wisdom Star app. Here are the steps on how to install and run this app on your vps.

### Run Nighttime Wisdom Star

1. Enter the sudo mode of vps

2. Ubuntu downloads the install_docker_and_compose_ubuntu.sh file,

    instruction:

    ```bash
    wget https://github.com/14790897/Nighttime-Wisdom-Star/raw/main/install_docker_and_compose_ubuntu.sh
    ```

    centos download install_docker_and_compose_centos.sh file

    instruction:

    ```bash
    wget https://github.com/14790897/Nighttime-Wisdom-Star/raw/main/install_docker_and_compose_centos.sh
    ```

3. Run the following command:

    ubuntu:

    ```bash
    .install_docker_and_compose_ubuntu.sh
    ```

    centos:

    ```bash
    .install_docker_and_compose_centos.sh
    ```

    The system will prompt you to enter the corresponding environment variables, please follow the prompts.

4. Wait for Docker Compose to pull the required images and start the service, this may take some time depending on your network speed and machine performance.
5. When all services are started, you can use the Nighttime Wisdom Star application by visiting [http://vpsIP:5001](http://vpsIP:5001) through a browser.

## FQA

1. If you want to view all the data of registered users?

    Run the following command:

    ```bash
    docker-compose exec redis sh
    ```

    Enter `redis-cli`, enter the database, and then ask ChatGPT how to view redis data.

2. How to modify the running time, the total number of answers, etc. again?

    Modify the corresponding value in the .env file, and run the following command to update after completion:

    ```bash
    docker-compose down
    ```

    ```bash
    docker-compose up
    ```

    If you encounter any problems during use, or have any suggestions, welcome to file an issue.

### Thanks!



## How to use (old version, complex, not recommended, suitable for users who don't know how to use docker, but it is not perfect yet)

Change .env.template to .env and fill in the corresponding parameters. SECRET_KEY can be generated at will, and the URL is the domain name of your own server Pandora project, or you will not configure a domain name. You can also replace it with the IP: port of the running Pandora project.

### Simplified steps (this script is not yet complete):

```
chmod +x script.sh
./script.sh
```

### Specific steps:

#### Install my project

Assuming your vps is an Ubuntu system,

In the /home/ubuntu directory (the directory is optional, but be careful to operate in the same directory), download my GitHub project

```
git clone https://github.com/14790897/Nighttime-Wisdom-Star.git
```

Modify `host=redis_host` in app.py (please use the search function to find this line) to `host='localhost'`

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

Press i to enter insert mode, copy the following content, ctrl+shift+v paste, so that the project can run in the background

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

Press esc, enter: wq, press Enter, save and exit the editor

start running command

```
systemctl start myapp
```

Enter the following command on the command line to make it start automatically

```
systemctl enable myapp
```

#### Install Pandora

Download the Pandora project

```
git clone https://github.com/pengzhile/pandora.git
```

Then background the project

```
vim /etc/systemd/system/pandora.service
```

As before, copy the following into

```
[Unit]
Description=Pandora Service
After=network.target

[Service]
ExecStart=/usr/local/bin/pandora -t t.json -s 0.0.0.0:8008
Restart=always
# need to be replaced according to the actual path
WorkingDirectory=/home/ubuntu

[Install]
WantedBy=multi-user.target
```

start running command

```
systemctl start myapp
```

boot command

```
systemctl enable myapp
```

Create a t.json file in the /home/ubuntu directory, and enter the account access token obtained by cracking https://chat.openai.com/api/auth/session.

#### Install redis database.

omit...

### Congratulations, you're done

Next, you can configure nginx according to your needs. You can use domain name access (this tutorial will not teach), or you can access directly by IP: port (port is 5000).