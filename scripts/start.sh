#!/bin/sh

# Log start message
echo "YT2Plex erfolgreich gestartet" >> /var/log/cron.log
echo "Dein Google API Key ist: $API_KEY" >> /var/log/cron.log

# Write API_KEY to file
echo $API_KEY > /scripts/apikey.txt

# Add the cron job
echo "*/30 * * * * /usr/local/bin/python /scripts/main.py >> /var/log/cron.log 2>&1" > /etc/cron.d/yt2plex-cron

# Apply cron job
crontab /etc/cron.d/yt2plex-cron

# Start cron and tail logs
cron && tail -f /var/log/cron.log

