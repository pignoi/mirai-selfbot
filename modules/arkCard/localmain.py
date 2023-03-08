from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from modules.arkCard.doRandom import arkGetCard
import json

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    cmds = json.load(open("modules/arkCard/config.json"))["basic"]["cmd"]
    admincmds = json.load(open("modules/arkCard/config.json"))["basic"]["admincmd"]
    user_cmd = message.display.split()[0]
    if user_cmd in admincmds:
        if message.display.split()[1] == "查询卡池":
            opening_pool = json.load(open("modules/arkCard/config.json"))["basic"]["cmd"]
            await app.send_group_message(
                group,
                MessageChain(f'正在开放的卡池有：{"，".join(opening_pool)}'))
    
    if user_cmd in cmds:
        
        user_times = message.display.split()[1]
        user_nosix = message.display.split()[2]
        if int(user_times) > 100 or int(user_nosix) > 100:
            await app.send_group_message(
            group,
            MessageChain("数据错误，仅限100次以下的抽卡，未出六星次数也应当小于100."))
        
        else:
            if user_cmd == "常驻池":
                result = arkGetCard(user_times, user_nosix).norm_pool()
            if user_cmd == "怪猎限定池":
                result = arkGetCard(user_times, user_nosix).pool_120()
            if user_cmd == "春节限定池":
                result = arkGetCard(user_times, user_nosix).limit_pool(pooltype="春节")

            final_result = []

            for i in result:
                for p in i:final_result.append(p)
            await app.send_group_message(
                group,
                MessageChain(final_result))
    else:
        return 