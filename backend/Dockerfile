FROM python:3.11

ARG ENV=dev
ENV ENV=${ENV}

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Install cron and tzdata to set the timezone
RUN apt-get update && apt-get install -y cron tzdata && apt-get clean

# set timezone
ENV TZ=Europe/Paris
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . .

COPY services/crontab /etc/cron.d/crontab
COPY entrypoint.sh /entrypoint.sh

# Permissions
RUN chmod +x /entrypoint.sh
RUN chmod 0644 /etc/cron.d/crontab
RUN touch /var/log/cron.log

# Define the entrypoint
ENTRYPOINT ["/entrypoint.sh"]
