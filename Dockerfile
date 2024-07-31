FROM python:3.9-slim AS base

RUN pip install google-api-python-client yt-dlp

# Install cron
RUN apt-get update && apt-get install -y cron

# Copy your scripts and data into the container
COPY scripts /scripts

# Set environment variable
#ENV API_KEY=your_api_key_here

# Add labels for mandatory volumes and environment variables
LABEL com.docker.compose.volumes.playlist="Playlist volume"
LABEL com.docker.compose.volumes.channels="Channels volume"
LABEL com.docker.compose.environment.API_KEY="API Key"

VOLUME /scripts/playlist
VOLUME /scripts/channels

# Create the log file to be able to run tail
RUN touch /var/log/cron.log
RUN touch /scripts/playlist/guide.xml
RUN touch /scripts/playlist/playlist.m3u
RUN touch /scripts/channels/channels.txt
RUN touch /scripts/channels/channels.json

# Give execution rights on the cron job
RUN chmod +x /scripts/main.py

# Give permission on cron log
RUN chmod 666 /var/log/cron.log

# Give execution rights on the
RUN chmod +x /scripts/start.sh

# Give execution rights on the Get-Channels.py
RUN chmod +x /scripts/Get-Channels.py

# Run the command on container startup
CMD ["/scripts/start.sh"]

