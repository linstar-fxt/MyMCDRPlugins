import re
from mcdreforged.api.all import *

PLUGIN_METADATA = {
	'id': 'whoisdied',
	'version': '2.0.1',
	'name': 'WhoIsDied',
	'author': [
		'hai122',
		'linstar'
    ],
	'link': 'https://github.com/linstar-fxt/MyMCDRPlugins/tree/main/WhoIsDied',
    'dependencies' :  {
	    'mcdreforged': '>=1.0.0',
	    'minecraft_data_api': '*'
    }   
}


DeathMessage = [
"(\\w{1,16}) blew up",
"(\\w{1,16}) burned to death",
"(\\w{1,16}) didn't want to live in the same world as .+",
"(\\w{1,16}) died",
"(\\w{1,16}) died because of .+",
"(\\w{1,16}) discovered floor was lava",
"(\\w{1,16}) discovered the floor was lava",
"(\\w{1,16}) drowned",
"(\\w{1,16}) drowned whilst trying to escape .+",
"(\\w{1,16}) experienced kinetic energy",
"(\\w{1,16}) experienced kinetic energy whilst trying to escape .+",
"(\\w{1,16}) fell from a high place",
"(\\w{1,16}) fell off a ladder",
"(\\w{1,16}) fell off a scaffolding",
"(\\w{1,16}) fell off some twisting vines",
"(\\w{1,16}) fell off some vines",
"(\\w{1,16}) fell off some weeping vines",
"(\\w{1,16}) fell out of the water",
"(\\w{1,16}) fell out of the world",
"(\\w{1,16}) fell too far and was finished by .+",
"(\\w{1,16}) fell too far and was finished by .+ using .+",
"(\\w{1,16}) fell while climbing",
"(\\w{1,16}) hit the ground too hard",
"(\\w{1,16}) hit the ground too hard whilst trying to escape .+",
"(\\w{1,16}) starved to death",
"(\\w{1,16}) starved to death whilst fighting .+",
"(\\w{1,16}) suffocated in a wall",
"(\\w{1,16}) suffocated in a wall whilst fighting .+",
"(\\w{1,16}) tried to swim in lava",
"(\\w{1,16}) tried to swim in lava to escape .+",
"(\\w{1,16}) walked into a cactus whilst trying to escape .+",
"(\\w{1,16}) walked into danger zone due to .+",
"(\\w{1,16}) walked into fire whilst fighting .+",
"(\\w{1,16}) walked on danger zone due to .+",
"(\\w{1,16}) was blown up by .+",
"(\\w{1,16}) was blown up by .+ using .+",
"(\\w{1,16}) was burnt to a crisp whilst fighting .+",
"(\\w{1,16}) was doomed to fall",
"(\\w{1,16}) was doomed to fall by .+",
"(\\w{1,16}) was doomed to fall by .+ using .+",
"(\\w{1,16}) was fireballed by .+",
"(\\w{1,16}) was fireballed by .+ using .+",
"(\\w{1,16}) was impaled by Trident",
"(\\w{1,16}) was impaled by .+",
"(\\w{1,16}) was impaled by .+ with .+",
"(\\w{1,16}) was killed by [Intentional Game Design]",
"(\\w{1,16}) was killed by .+ trying to hurt .+",
"(\\w{1,16}) was killed by .+ using .+",
"(\\w{1,16}) was killed by .+ using magic",
"(\\w{1,16}) was killed by even more magic",
"(\\w{1,16}) was killed by magic",
"(\\w{1,16}) was killed by magic whilst trying to escape .+",
"(\\w{1,16}) was killed trying to hurt .+",
"(\\w{1,16}) was poked to death by a sweet berry bush",
"(\\w{1,16}) was poked to death by a sweet berry bush whilst trying to escape .+",
"(\\w{1,16}) was pricked to death",
"(\\w{1,16}) was pummeled by .+",
"(\\w{1,16}) was pummeled by .+ using .+",
"(\\w{1,16}) was roasted in dragon breath",
"(\\w{1,16}) was roasted in dragon breath by .+",
"(\\w{1,16}) was shot by Arrow",
"(\\w{1,16}) was shot by .+",
"(\\w{1,16}) was shot by .+ using .+",
"(\\w{1,16}) was slain by Arrow",
"(\\w{1,16}) was slain by Small Fireball",
"(\\w{1,16}) was slain by Trident",
"(\\w{1,16}) was slain by .+ and (\\w{1,16}) was slain by (\\w{1,16}).",
"(\\w{1,16}) was slain by .+ using .+ and (\\w{1,16}) was slain by (\\w{1,16}) using .+.",
"(\\w{1,16}) was slain by .+",
"(\\w{1,16}) was slain by .+ using .+",
"(\\w{1,16}) was slain by (\\w{1,16}) using .+",
"(\\w{1,16}) was squashed by .+",
"(\\w{1,16}) was squashed by a falling anvil",
"(\\w{1,16}) was squashed by a falling anvil whilst fighting .+",
"(\\w{1,16}) was squashed by a falling block",
"(\\w{1,16}) was squashed by a falling block whilst fighting .+",
"(\\w{1,16}) was squished too much",
"(\\w{1,16}) was struck by lightning",
"(\\w{1,16}) was struck by lightning whilst fighting .+",
"(\\w{1,16}) was stung to death",
"(\\w{1,16}) was stung to death by .+",
"(\\w{1,16}) went off with a bang",
"(\\w{1,16}) went off with a bang whilst fighting .+",
"(\\w{1,16}) went up in flames",
"(\\w{1,16}) withered away",
"(\\w{1,16}) withered away whilst fighting .+"
]

dim_convert = {
    0: '§a主世界§r',
    -1: '§c下界§r',
    1: '§5末地§r'
}

@new_thread(PLUGIN_METADATA['name'])
def on_info(server: ServerInterface, info: Info):
    if info.is_user:
        return
    for item in DeathMessage:
        re_exp = re.fullmatch(item, info.content)
        if re_exp:
            player = re_exp.group(1)
            if 'carpetbotlist' in server.get_plugin_list():
                botApi = server.get_plugin_instance('carpetbotlist')
                botlist = botApi.list_bot(server)
                if botlist and player in botlist:
                    return
            send_mesage(player, server)
            return
    
def send_mesage(player, server):
    api = server.get_plugin_instance('minecraft_data_api')
    server.say(f"<{player}> awsl")
    dim = api.get_player_dimension(player)
    cord = api.get_player_coordinate(player)
    if dim == 0:
        server.say('§6{} §7@ {} [x:{}, y:{}, z:{}] --> §c下界§r [x:{}, y:{}, z:{}]'.format(player, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z), int((cord.x)/8), int(cord.y), int((cord.z)/8)))
    elif dim == -1:
        server.say('§6{} §7@ {} [x:{}, y:{}, z:{}] --> §a主世界§r [x:{}, y:{}, z:{}]'.format(player, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z), int((cord.x)*8), int(cord.y), int((cord.z)*8)))
    elif dim == 1:
        server.say('§6{} §7@ {} [x:{}, y:{}, z:{}]'.format(player, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z)))
