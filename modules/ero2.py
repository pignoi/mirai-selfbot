from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from graia.ariadne.event.mirai import NudgeEvent

import random

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[NudgeEvent]))
async def getup(app: Ariadne, event: NudgeEvent):
    mess = ["八嘎hentai无路赛","yamairo","你不要光天化日之下在这里戳我啊","别戳了，好痒~"]
    return_mes = random.choice(mess)
    if event.subject["kind"] == "Group":
        
        await app.send_group_message(
            event.group_id,
            MessageChain(return_mes)
        )
    elif event.subject["kind"] == "Friend":
        
        await app.send_friend_message(
            event.friend_id,
            MessageChain(return_mes)
        )
    else:
        return
