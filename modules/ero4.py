from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import openai
import os

openai.api_key = os.getenv("GPT_KEY")
def sendToOpenai(question):

    completions = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
        {"role": "user", "content": f"{question}"},
    ]
)

    resMes = completions.choices[0].message.content
    return 1,resMes

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display[0:3] == "ai ":
        await app.send_message(
                group,
                MessageChain(f"已收到，请稍等返回信息。"),
             )
        status_code, res = sendToOpenai(message.display[3:])
        if status_code == 1:
            await app.send_message(
                group,
                MessageChain(f"(以下回答均源自于openai gpt-3.5-turbo模型，和帐号持有者无关，不代表帐号持有者的任何立场）\n{res}"),
             )
        if status_code ==0:
            await app.send_message(
                group,
                MessageChain(f"{res}"),
             )
    else:
        return 