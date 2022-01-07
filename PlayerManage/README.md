### PlayerManage 帮助你管理玩家

#### 功能：
- 玩家基本信息预览
- Bot快捷指令面板
- 玩家在线时间排行
- 玩家得分统计

#### Api：
```python -> bool
def isBot(name:str): -> bool
``` 
提供对bot的判别

```python
def get_player_data(uuid:str, path=None):
```
获取储存在PlayerData文件夹的玩家数据，其中path只支持一层key，如发生错误则返回None

```python
def get_stat_data(uuid: str, filter=None):
````
获取储存在Stats文件夹下的玩家得分，其中filter为None时，返回data['stats']，为key时，返回列表[data['stats'][key],所有值的和],为两层key时，返回对应的值    
示例： 获取minecraft:deaths
```python
get_stat_data(uuid,"custom.deaths")
```


