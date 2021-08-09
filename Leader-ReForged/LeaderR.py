import time
from mcdreforged.api.all import *
from mcdreforged.plugin.server_interface import ServerInterface
from mcdreforged.info import Info

PLUGIN_METADATA = {
    'id': 'leaderreforged',
    'version': '1.0.0',
    'name': 'LeaderR',
    'author': 'linstar-fxt',
    'link': 'https://github.com/linstar-fxt/MyMCDRPlugins/tree/main/Leader-ReForged',
    'dependencies': {
            'mcdreforged': '>=1.0.0',
            'minecraft_data_api': '>= 1.3.0'
    }
}

dim_convert = {
    0: '§a主世界§r',
    -1: '§c下界§r',
    1: '§5末地§r'
}

LeaderStat = False
Leader = None

@new_thread(PLUGIN_METADATA['name'])

def leader(src: CommandSource):
    global LeaderStat
    global Leader
    if not src.is_player:
        src.reply('§c控制台不能变成引领者!')
        return
    if LeaderStat:
        src.reply('§c已经存在引领者了!引领失败')
        return
    LeaderStat = True
    Leader = src.player   #等待验证
    server = src.get_server()
    api = server.get_plugin_instance('minecraft_data_api')
    dim = api.get_player_dimension(Leader)
    cord = api.get_player_coordinate(Leader)

    server.say('[LeaderR] 已标记玩家§b {} §r为引导者,快跟随他叭~'.format(Leader))
    server.execute('effect give {} minecraft:glowing 9999 1'.format(Leader))
    src.reply('§7[LeaderR] 你成为了引导者,每隔60秒将广播坐标')
    src.reply('§7[LeaderR] 使用!!unleader取消引领')
    pos_Leader(server, dim, cord, Leader)
    while LeaderStat:
        time.sleep(60)
        if not LeaderStat:
            break
        else:
            src.reply('§7 [LeaderR]引领者每隔60秒广播坐标，使用!!unleader取消引领')
            pos_Leader(server, dim, cord, Leader)
    
def pos_Leader(server, dim, cord, Leader):
    if dim == 0:
        server.say('§6 引领者{} §7@ {} [x:{}, y:{}, z:{}] -> §c下界§r [x:{}, y:{}, z:{}]'.format(Leader, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z), int((cord.x)/8), int(cord.y), int((cord.z)/8)))
    elif dim == -1:
        server.say('§6 引领者{} §7@ {} [x:{}, y:{}, z:{}] -> §a主世界§r [x:{}, y:{}, z:{}]'.format(Leader, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z), int((cord.x)*8), int(cord.y), int((cord.z)*8)))
    elif dim == 1:
        server.say('§6 引领者{} §7@ {} [x:{}, y:{}, z:{}]'.format(Leader, dim_convert[dim], int(cord.x), int(cord.y), int(cord.z)))
    else:
        return

def unleader(src: CommandSource):
    global LeaderStat
    global Leader
    server = src.get_server()

    if LeaderStat and Leader == src.player:
        LeaderStat = False
        server.execute('effect clear {} minecraft:glowing'.format(Leader))
        server.say("[LeaderR] §b{} §r已经取消引领，不要再打扰他了!".format(Leader))
        Leader = None
    else:
        src.reply('§c你不是引领者!')

def on_load(server: ServerInterface, prev):
    server.register_help_message('!!leader', '成为一名引领者')         
    server.register_help_message('!!unleader', '放弃成为一名引领者')      
    server.register_command(Literal('!!leader').runs(leader))            
    server.register_command(Literal('!!unleader').runs(unleader))           
