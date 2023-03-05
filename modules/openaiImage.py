from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group
from graia.ariadne.message.element import Image

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import openai
import os

import requests
from io import BytesIO

openai.api_key = os.getenv("GPT_KEY")
def sendToOpenai(question):

    completions =  openai.Image.create(
        prompt=f"{question}",
        n=1,
        size="256x256"
    )
    image_url = completions['data'][0]['url']

    resMes = image_url
    return 1,resMes

def get_picbytes(url):
    headers = {"Content-Type": "bytes"}
    response = requests.get(url, headers=headers)
    data = BytesIO(response.content)

    return data

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display[0:4] == "aiI ":
        await app.send_message(
                group,
                MessageChain(f"已收到，请稍等返回信息，由于未知原因图片返回速度较慢，反应期间的命令依然能够接收。"),
             )
        status_code, res = sendToOpenai(message.display[4:])
        if status_code == 1:
            data = get_picbytes(res)
            await app.send_message(group, MessageChain(
                        Image(data_bytes=data)
                        ))
            
        if status_code ==0:
            await app.send_message(
                group,
                MessageChain(f"{res}"),
             )
    else:
        return 