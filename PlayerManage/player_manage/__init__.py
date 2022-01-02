import re, collections
from datetime import timedelta, datetime

from mcdreforged.api.all import *

from player_manage.config import Config
from player_manage.model import creat_database,session,Player
from player_manage.util import get_player_data, get_stat_data, get_uuid

config:Config
botList = []

def on_load(server:PluginServerInterface,old):
    global config,botList
    config = server.load_config_simple("config.json",in_data_folder=True, target_class=Config)
    Config.set_instance(config)

    creat_database()
    botList = session.query(Player.name).filter(Player.is_bot == True).all()

    server.register_help_message(config.prefix,"帮助你管理玩家")
    server.register_command(
        Literal(config.prefix).runs(sendHelp)
        .then(Literal("list").then(QuotableText('type').runs(lambda src,ctx:sendList(src,ctx['type']))))
        .then(Literal("listol").then(QuotableText('type').runs(lambda src,ctx:sendList(src,ctx['type'],online=True))))
        .then(Literal("query").then(QuotableText('player').runs(lambda src,ctx: send_player_data(src,ctx['player']))))
        .then(Literal("stats").then(QuotableText('player').runs(lambda src,ctx: send_player_stats(src,ctx['player']))))
        .then(Literal('board').then(QuotableText('type').runs(lambda src,ctx: send_player_board(src,ctx['type']))))
        .then(Literal("shadow").then(QuotableText('bot').runs(lambda src,ctx:shadowPlayer(src,ctx['bot']))))
    )

def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    login_update(info,player)

def sendHelp(src:CommandSource):
    prefix = config.prefix
    msg = f'''
    ------------§aCommand Useage§r---------------
    | {prefix} - Show this help message
    | {prefix} list <bot/player/all>- List all players
    | {prefix} listol <bot/player/all>- List all online players
    | {prefix} query <Player> - Query player infomation
    | {prefix} board <bot/player/all>- Player Online Time Leaderboard
    | {prefix} stats <player> - Show all the points
    | {prefix} shadow <player> - Let bot look in the same direction as you
    '''
    src.reply(msg)

@new_thread("PlayerManage")
def sendList(src:CommandSource,type:str,online=False):
    types = {
        'bot':True,
        'player':False,
        'all':None
    }
    players=[]
    try:
        type = types[type]
    except:
        src.reply("错误的参数")
        return
    if not type:
        for item in session.query(Player.name).all():
            players.append(item[0])
    else:
        for item in session.query(Player.name).filter(Player.is_bot == type).all():
            players.append(item[0])

    server = src.get_server()
    dataapi = server.get_plugin_instance("minecraft_data_api")
    playerList = dataapi.get_server_player_list()[-1] if online else players
    src.reply("§aServer Players")
    for player in players:
        if not player in playerList:
            continue 
        lis = RTextList(RText(f'·{player}').set_hover_text(
            RText('·单击以查看信息和编辑')
            ).set_click_event(
                RAction.run_command,f'{config.prefix} query {player}'
            )
        )
        src.reply(lis)

@new_thread("PlayerManage")
def send_player_data(src:CommandSource,name:str):
    server = src.get_server()
    dataapi = server.get_plugin_instance("minecraft_data_api")
    playerList = dataapi.get_server_player_list()[-1]
    online = name in playerList

    thisPlayer = session.query(Player).filter(Player.name == name).first()
    playerData = dataapi.get_player_info(name) if online and dataapi.get_player_info(name) is not None else get_player_data(thisPlayer.uuid)
    x = float(str(playerData["Pos"][0]))
    y = float(str(playerData["Pos"][1]))
    z = float(str(playerData["Pos"][2]))
    x1 = float(str(playerData["Rotation"][0]))
    y1 = float(str(playerData["Rotation"][1]))
    dim = str(playerData["Dimension"])
    playTime = int(int(get_stat_data(thisPlayer.uuid,"custom.play_one_minute")) / 20)
    leaveGame = get_stat_data(thisPlayer.uuid,"custom.leave_game")
    if leaveGame is not None:
        leaveGame = int(playTime / leaveGame)
    msg = [
        RText('§a======================'),
        RTextList(
            RText(f'§b{name}').set_hover_text(
                RTextList(
                    RText('类型:假人' if thisPlayer.is_bot else '类型:玩家'),
                    RText(f'UUID:{thisPlayer.uuid}')
                )
            ),
            RText('     level:§a{}'.format(str(playerData['XpLevel']))),
            RText('-饱食度:§a{}'.format(str(playerData['foodLevel'])))
        ),
        #RText('累计上线时间:§b%d:%02d:%02d'%(h,m,s)),
        RText('累计上线时间:§b{}'.format(str(timedelta(seconds=playTime)))),
        RText('最近一次上线时间:§b{}'.format((thisPlayer.lastjoin + timedelta(hours=int(config.timezone))).strftime("%Y-%m-%d %H:%M:%S"))),
        RText('平均每次上线游玩时间:§b{}'.format(str(timedelta(seconds=leaveGame)))),
        RText(f'坐标:§b[x:{x},y:{y},z:{z},dim:"{dim}"]'),
        RTextList(
            RText('§4[x]§f ' if thisPlayer.is_bot else '').set_hover_text(
                "删除这个假人"
            ).set_click_event(
                RAction.run_command,f'/player {name} kill'
            ),
            RText('[U] ' if thisPlayer.is_bot else '').set_hover_text(
                "使用这个假人"
            ).set_click_event(
                RAction.run_command,f'/player {name} use'
            ),
            RText("[R] " if thisPlayer.is_bot and not online else '').set_hover_text(
                "在假人的下线位置重新生成假人"
                "PS:无法跨维度重新生成！"
            ).set_click_event(
                RAction.run_command,f'/player {name} spawn at {x} {y} {z} facing {x1} {y1}'
            ),
            RText("[M]" if thisPlayer.is_bot else '').set_hover_text(
                "让假人面朝方向和你一样"
            ).set_click_event(
                RAction.run_command,f'!!player {name} -shadow'
            )
        )
    ]
    for item in msg:
        src.reply(item)

@new_thread("PlayerManage-Web")
def login_update(info:Info,player:str):
    re_info = re.match(r"(\w+)\[([0-9\.\:\/]+|local)\] logged in with entity id", info.content)
    if not re_info:
        return

    isBot = True if re_info.group(2) == "local" else False
    if isBot: 
        botList.append(player)

    joined_player = session.query(Player).filter(Player.name == player).first()

    if joined_player:
        joined_player.is_bot = isBot
        joined_player.lastjoin = datetime.utcnow()
        session.commit()
    else:
        new_player = Player(
            name = player,
            firstjoin = datetime.utcnow(),
            lastjoin = datetime.utcnow(),
            uuid = get_uuid(player),
            is_bot = isBot
        )
        session.add(new_player)
        session.commit()

@new_thread("PlayerManage")
def shadowPlayer(src:CommandSource,bot:str):
    if not src.is_player:
        return
    server = src.get_server()
    dataapi = server.get_plugin_instance("minecraft_data_api")
    Rotation = dataapi.get_player_info(str(src).split[' '][1], "Rotation") if dataapi.get_player_info(str(src).split[' '][1], "Rotation") is not None else [0,0]
    server.execute(f'/player {bot} look {Rotation[1]} {Rotation[0]}')

def send_player_stats(src:CommandSource, player:str):
    uuid = session.query(Player.uuid).filter(Player.name == player).first()[0]
    mined = get_stat_data(uuid,"mined")
    msg = [
        RText(f" §a{player} 的统计点"),
        RText("| 挖掘方块:{}".format(mined[1] if mined else None)),
        RText("| 死亡次数:{}".format(get_stat_data(uuid,"custom.deaths"))),
        RText("| 交易次数:{}".format(get_stat_data(uuid,"custom.traded_with_villager"))),
        RText("| 睡觉次数:{}".format(get_stat_data(uuid,"custom.sleep_in_bed")))
    ]
    for item in msg:
        src.reply(item)

def send_player_board(src:CommandSource,type:str):
    types = {
        'bot':True,
        'player':False,
        'all':None
    }
    players={}
    try:
        type = types[type]
    except:
        src.reply("错误的参数")
        return
    if not type:
        for item in session.query(Player.name,Player.uuid).all():
            players[item[1]] = item[0]
    else:
        for item in session.query(Player.name,Player.uuid).filter(Player.is_bot == type).all():
            players[item[1]] = item[0]
    
    if not players:
        src.reply("还没有在案玩家")
        return
    points = {}
    for uuid in players.keys():
        point = get_stat_data(uuid,"custom.play_one_minute")
        points[players[uuid]] = point if point else 0
    
    points = collections.Counter(points).most_common()
    src.reply(" 爆肝排行！")
    for item in points:
        src.reply(f"·{item[0]}: §a{str(timedelta(seconds=int(item[1]/20)))}")

def isBot(name:str): 
    if name in botList:
        return True
    return False