from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

channel = Channel.current()


@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display[0:4] == "记住了，":
        u_mes = message.display.split("，")
        if len(u_mes) < 3:
            re_mes = "格式错误，请按照“记住了，*命令语句*，*回答语句*”的格式训练我哦"
        else:
            key = message.display.split("，")[1]
            answer = message.display.split("，")[2]
            with open("modules/ero3.data","a+") as f:
                f.write(f"{key}$split${answer}\n")
            re_mes = "记住了！"
        await app.send_message(
            group,
            MessageChain(f"{re_mes}"),
         )
    if message.display[0:3] == "你说，":
        u_ans = []
        
        u_key = message.display[3:]
        with open("modules/ero3.data") as f:
            q = f.readlines()[::-1]
            
        for i in q:
            s_key = i.split("$split$")[0]
            if s_key == u_key:
                u_ans.append(i.split("$split$")[1][:-1])
        if u_ans == []:   
            await app.send_message(
                group,
                MessageChain("人家不知道哦~"),
            )
        else:
            await app.send_message(
                group,
                MessageChain(" ".join(u_ans)),
            )
    else:
        return 