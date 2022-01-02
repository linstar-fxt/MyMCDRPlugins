import requests, os
from urllib.request import urlopen
import ujson as json
from uuid import UUID

from nbt import nbt
from player_manage.config import Config

def get_uuid(name:str):
    try:
        data = requests.get(url=f'https://api.mojang.com/users/profiles/minecraft/{name}').json() #Online
        return str(UUID(data['id']))
    except Exception as e:
        print(e)
        data = requests.get(url=f'http://tools.glowingmines.eu/convertor/nick/{name}').json() #Offline
        return str(data['offlinesplitteduuid'])

def get_player_data(uuid:str, path=None):
    try:
        nbtfile = nbt.NBTFile(os.path.join(Config.get_instance().get_world_path(), 'playerdata', f'{uuid}.dat'))
        if path:
            nbtfile = nbtfile[path]
        return nbtfile
    except:
        return None

def get_stat_data(uuid: str, filter=None):
    try:
        with open(os.path.join(Config.get_instance().get_world_path(), 'stats', f'{uuid}.json'), 'r') as file:
            if not filter:
                return json.load(file)['stats']
            if not '.' in filter:
                data = json.load(file)['stats']['minecraft:'+filter]
                point = 0
                for item in data.values():
                    point += int(item)
                return [data, point]
            filter = filter.split('.')
            return json.load(file)['stats']['minecraft:'+filter[0]]['minecraft:'+filter[1]]
    except Exception as e:
        print(e)
        return None

