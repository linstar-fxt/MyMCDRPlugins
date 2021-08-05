import json
import re
import time
from mcdreforged.api.all import *
from typing import List

PLUGIN_METADATA = {
	'id': 'whoisdied',
	'version': '2.0.0',
	'name': 'WhoIsDied',
	'author': [
		'hai122',
		'linstar'
    ],
	'link': 'https://github.com/linstar-fxt/WhoIsDied-MCDR',
    'dependencies' :  {
	    'mcdreforged': '>=1.0.0',
	    'minecraft_data_api': '*'
    }   
}

HIGHLIGHT_TIME = 0

DeathMessage = [
    " blew up",
    " burned to death",
    " didn't want to live in the same world as",
    " died",
    " died because of",
    " discovered floor was lava",
    " discovered the floor was lava",
    " drowned",
    " drowned whilst trying to escape",
    " experienced kinetic energy",
    " fell from a high place",
    " fell off a ladder",
    " fell off a scaffolding",
    " fell off some twisting vines",
    " fell off some vines",
    " fell off some weeping vines",
    " fell out of the water",
    " fell out of the world",
    " fell too far and was finished by",
    " fell while climbing",
    " hit the ground too hard",
    " hit the ground too hard whilst trying to escape",
    " starved to death",
    " suffocated in a wall",
    " tried to swim in lava",
    " walked into a cactus whilst trying to escape",
    " walked into danger zone due to",
    " walked into fire whilst fighting",
    " walked on danger zone due to",
    " was blown up by",
    " was burnt to a crisp whilst fighting",
    " was doomed to fall",
    " was fireballed by",
    " was impaled by",
    " was killed by",
    " was killed trying to hurt",
    " was poked to death by a sweet berry bush",
    " was poked to death by a sweet berry bush whilst trying to escape",
    " was pricked to death",
    " was pummeled by",
    " was roasted in dragon breath",
    " was shot by",
    " was slain by",
    " was squashed by",
    " was squished too much",
    " was struck by",
    " was stung to death",
    " went off with a bang",
    " went up in flames",
    " withered away",
    " withered away whilst fighting"
]

dim_convert = {
    0: '§a主世界§r',
    -1: '§c下界§r',
    1: '§5末地§r'
}

@new_thread(PLUGIN_METADATA['name'])

#服务器info监听函数
def on_info(server, info):
    global tmp5
    pl = False
    api = server.get_plugin_instance('minecraft_data_api')
    if info.is_player:
        return
    if "[Server thread/INFO]" in str(info):
        for Died in DeathMessage:
            if Died in str(info):
                #server.say("wdwhu")
                #server.say(Died)
                pl = True
                break      
    else:
        return

    if not pl:
        return
    
    pl = False

    amount, limit, players = api.get_server_player_list()
    if players == None or players == []:
        return
    for player in players:
        if player in str(info):
            pl = True
            break    
    
    if not pl:
        return

    if pl:
        server.say('<{}> awsl'.format(player))
        dim = api.get_player_dimension(player)
        cord = api.get_player_coordinate(player)
        if dim == 0:
            server.say('§6{} §7@ {} [x:{}, y:{}, z:{}] --> §c下界§r [x:{}, y:{}, z:{}]'.format(player, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z), int((cord.x)/8), int(cord.y), int((cord.z)/8)))
        elif dim == -1:
            server.say('§6{} §7@ {} [x:{}, y:{}, z:{}] --> §a主世界§r [x:{}, y:{}, z:{}]'.format(player, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z), int((cord.x)*8), int(cord.y), int((cord.z)*8)))
        elif dim == 1:
            server.say('§6{} §7@ {} [x:{}, y:{}, z:{}]'.format(player, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z)))
        
        if not HIGHLIGHT_TIME == 0:
            server.execute('effect give {} minecraft:glowing {} 1'.format(player, HIGHLIGHT_TIME))
    else:
        return
