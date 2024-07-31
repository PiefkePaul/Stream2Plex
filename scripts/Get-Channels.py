import os
import json
import requests
import re
import sys

# Ausgabe in eine Log-Datei umleiten
sys.stdout = open('/var/log/cron.log', 'a')
sys.stderr = open('/var/log/cron.log', 'a')

# Funktion, um den API-Schlüssel aus einer Datei zu lesen
def get_api_key(api_key_path):
    with open(api_key_path, 'r') as file:
        return file.read().strip()

# Funktion, um die Kanal-ID anhand des Handles zu finden
def get_channel_id_by_handle(api_key, handle):
    url = 'https://www.googleapis.com/youtube/v3/search'
    params = {
        'part': 'snippet',
        'q': handle,
        'type': 'channel',
        'key': api_key
    }
    response = requests.get(url, params=params)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        return data['items'][0]['id']['channelId']
    else:
        return None

# Funktion, um Kanaldetails mit der YouTube Data API abzurufen
def get_channel_details(api_key, channel_url):
    # Kanal-ID oder Name aus der URL extrahieren
    match = re.search(r'(channel/|@)([^/]+)', channel_url)
    if not match:
        return None
    channel_identifier = match.group(2)
    
    # Wenn es ein Handle ist, die Kanal-ID abrufen
    if '@' in channel_url:
        channel_identifier = get_channel_id_by_handle(api_key, channel_identifier)
        if not channel_identifier:
            return None
    
    # API-Endpunkt und Parameter definieren
    url = "https://www.googleapis.com/youtube/v3/channels"
    params = {
        'part': 'snippet',
        'id': channel_identifier,
        'key': api_key
    }
    
    # API-Anfrage senden
    response = requests.get(url, params=params)
    
    # JSON-Antwort parsen
    data = response.json()
    
    # Kanaldetails extrahieren
    if 'items' in data and len(data['items']) > 0:
        item = data['items'][0]
        thumbnails = item['snippet']['thumbnails']
        # Thumbnail mit der höchsten Qualität auswählen
        highest_quality_thumbnail = max(thumbnails.values(), key=lambda x: x['width'] * x['height'])
        channel_details = {
            'id': item['id'],
            'name': item['snippet']['title'],
            'icon': highest_quality_thumbnail['url']
        }
        return channel_details
    else:
        return None

# Funktion, um Kanal-URLs aus einer Datei zu lesen und deren Details abzurufen
def get_channels_details(channels_file_path, api_key_path):
    # API-Schlüssel abrufen
    api_key = get_api_key(api_key_path)
    
    # Kanal-URLs aus der Datei lesen
    with open(channels_file_path, 'r') as file:
        channel_urls = file.readlines()
    
    # Details für jeden Kanal abrufen
    channels_details = []
    for url in channel_urls:
        url = url.strip()
        details = get_channel_details(api_key, url)
        if details:
            channels_details.append(details)
    
    return channels_details

# Dateipfade definieren
channels_file_path = '/scripts/channels/channels.txt'
api_key_path = '/scripts/apikey.txt'
output_file_path = '/scripts/channels/channels.json'

# Kanaldetails abrufen und ausgeben
channels_details = get_channels_details(channels_file_path, api_key_path)

# Ergebnisse in die Datei schreiben
with open(output_file_path, 'w') as output_file:
    json.dump(channels_details, output_file, indent=4)

print(f"Kanaldetails wurden erfolgreich in {output_file_path} geschrieben.")

