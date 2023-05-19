FROM ubuntu:latest

# Update system and install dependencies
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    vim \
    git \
    redis-server

# Configure Redis
RUN if [ -f /etc/redis/redis.conf ]; then mv /etc/redis/redis.conf /etc/redis/redis.conf.bak; fi
RUN echo -e "save 900 1\nsave 300 10\nsave 60 10000\nstop-writes-on-bgsave-error no" > /etc/redis/redis.conf


# Create application directory
WORKDIR /home/ubuntu/app

# Clone your application
RUN git clone https://github.com/14790897/Nighttime-Wisdom-Star.git .

# Input access_token
run touch t.json
#ARG VARNAME
RUN #echo $VARNAME > t.json

# Install Python dependencies
RUN pip install -r requirements.txt

# Set up the environment variables
RUN mv .env.template .env
# RUN sed -i "s#URL=[^n]*#URL='127.0.0.1:8008'#g" .env
# RUN sed -i "s#SECRET_KEY=[^n]*#SECRET_KEY='477d75c5af744b76607fe86xcf8a5a368519acb486d62c5fa69bd42c16809f88'#g" .env

# Expose necessary ports
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
