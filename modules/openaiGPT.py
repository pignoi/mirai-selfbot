from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import openai
import aiohttp
import os
import asyncio

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

async def newSend(question):
    url = "https://api.openai.com/v1/chat/completions"
    headers = {'Content-Type': 'application/json',
               'Authorization': f'Bearer {os.getenv("GPT_KEY")}',
               }
    data = {"model": "gpt-3.5-turbo",
            "messages": [{"role": "user", "content": question}],
            "temperature": 0.7}
    session = Ariadne.service.client_session

    async with session.post(url=url, headers=headers, json=data) as response:
        ret = await response.json()
    status_code = response.status
    if status_code == 200:
        resMes = ret["choices"][0]["message"]["content"]
    else:
        resMes = "ERROR HASE!"

    return status_code, resMes

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display[0:3] == "ai ":
        await app.send_message(
                group,
                MessageChain(f"目前AI相关功能已恢复正常，请等待回复。"),
             )
        
        status_code, res = await newSend(message.display[3:])

        if status_code == 200:
            await app.send_message(
                group,
                MessageChain(f"(以下回答均源自于openai gpt-3.5-turbo模型，和帐号持有者无关，不代表帐号持有者的任何立场）\n{res}"),
             )
        if status_code != 200:
            await app.send_message(
                group,
                MessageChain(f"{res}"),
             )
    else:
        return 