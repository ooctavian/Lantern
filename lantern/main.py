import time
from lcu_driver import Connector
import requests
import ctypes
from pathlib import Path

connector = Connector()
r = requests.get('https://ddragon.leagueoflegends.com/api/versions.json')
data = r.json()
version = data[0]
r = requests.get(f"http://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json")
data = r.json()
champions = {}
for k in data['data']:
    champions[int(data['data'][k]['key'])] = k
summoner_id = 0
last_id = 0


def set_wallpaper(name, skin_id):
    request = requests.get(f'https://ddragon.leagueoflegends.com/cdn/img/champion/splash/{name}_{skin_id}.jpg')
    print(f"Downloading wallpaper: Champion - {name} SkinId - {skin_id}")
    home = str(Path.home())
    filepath = home + "\\AppData\\Local\\Temp\\lol_wallpaper_temp_background.jpg"
    open(filepath, 'wb').write(request.content)
    ctypes.windll.user32.SystemParametersInfoW(20, 0, filepath, 0)


@connector.ready
async def connect(connection):
    print('Connected to League client')
    global summoner_id
    request = await connection.request('GET', '/lol-summoner/v1/current-summoner')
    summoner_id = await request.json()
    while type(summoner_id != "<class 'dict'>") and 'displayName' not in summoner_id.keys():
        request = await connection.request('GET', '/lol-summoner/v1/current-summoner')
        summoner_id = await request.json()
        time.sleep(1)
    print(f"Connected as: {summoner_id['displayName']}")
    summoner_id = summoner_id['summonerId']


@connector.close
async def disconnect(_):
    print('Disconnected!')
    # await connector.stop()


@connector.ws.register('/lol-champ-select/v1/session', event_types=('UPDATE',))
async def change_wallpaper(_, event):
    global summoner_id
    global last_id
    for player in event.data['myTeam']:
        if player['summonerId'] == summoner_id and player['selectedSkinId'] != last_id:
            set_wallpaper(champions[player['championId']], player['selectedSkinId'] % 10)
            last_id = player['selectedSkinId']
            break


def main():
    connector.start()


if __name__ == "__main__":
    main()
