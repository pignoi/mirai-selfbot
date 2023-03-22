from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group,Member

import asyncio

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema
from graia.ariadne.message.element import At

import os, time
import json

import re

class oneCont:
    def __init__(self, group, member):
        self.timeout = 20*60
        self.group = group
        self.user = member
        self.now_time = time.time()

        self.jsonFile = f"modules/aicJSONs/{self.group}_{self.user}.json"

    def message(self):
        return self.group.id, self.user.id

    def start(self):
        if os.path.exists(self.jsonFile) == True:
            with open(self.jsonFile, "r") as f:
                jsonData = json.load(f)
                last_time = list(jsonData.keys())[-1]
                if jsonData[last_time]["status"] == "opening":
                    resMes = "上一个会话尚未结束，请继续上一个对话"

                elif jsonData[last_time]["status"] == "closed":
                    jsonData[str(self.now_time)] = {"status":"opening", "last_time":self.now_time, "history":["Hello, how can I help you?"]}
                    with open(self.jsonFile, "w") as fw:
                        fw.write(json.dumps(jsonData, indent=4, ensure_ascii=False))
                    resMes = "会话已开始，请按照“aic +提问内容”的格式进行连续问答"
        else:
            with open(self.jsonFile, "w") as f:
                jsonData = {str(self.now_time):{"status":"opening", "last_time":self.now_time, "history":["Hello, how can I help you?"]}}
                f.writable()
                f.write(json.dumps(jsonData, indent=4, ensure_ascii=False))

                resMes = "会话已开始，请按照“aic +提问内容”的格式进行连续问答"

        return resMes

    async def liaotian(self, user_input):
        if os.path.exists(self.jsonFile) == True:
            with open(self.jsonFile,"r") as f:
                jsonData = json.load(f)
                times = list(jsonData.keys())
                if jsonData[times[-1]]["status"] == "closed":
                    resMes = "没有正在进行的对话，请重新开始对话"

                elif self.now_time - float(jsonData[times[-1]]["last_time"]) > self.timeout:
                    resMes = "超时，请重新开始对话"
                    jsonData[times[-1]]["status"] = "closed"

                else:
                    history = jsonData[times[-1]]["history"]
                    if user_input == "exit":
                        jsonData[times[-1]]["status"] = "closed"
                        resMes = "对话已关闭。"
                    else:
                        history.append(user_input)
                        context = await self.getResolve(history)
                        response = context
                        response = await self.newSend(context, user_input)
                        resMes = response
                        history.append(response)

                        jsonData[times[-1]]["history"] = history
                        jsonData[times[-1]]["last_time"] = self.now_time
                with open(self.jsonFile,"w") as fw:
                    fw.write(json.dumps(jsonData, indent=4, ensure_ascii=False))

        else:
            resMes = "尚未开始对话"

        return resMes

    async def getResolve(self, historys):
        text = ' '.join(historys)
        text = re.sub('[^A-Za-z0-9]+', ' ', text)

        url = "https://api.openai.com/v1/chat/completions"
        headers = {'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.getenv("GPT_KEY")}',
                }
        data = {"model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": text}],
                "temperature": 0.7}

        session = Ariadne.service.client_session

        async with session.post(url=url, headers=headers, json=data) as response:
            ret = await response.json()
        status_code = response.status
        if status_code == 200:
            resMes = ret["choices"][0]["message"]["content"]
        else:
            resMes = f"{status_code}, ERROR HASE!"

        return resMes

    async def newSend(self, resolveResult, question):
        url = "https://api.openai.com/v1/chat/completions"
        headers = {'Content-Type': 'application/json',
                'Authorization': f'Bearer {os.getenv("GPT_KEY")}',
                }
        data = {"model": "gpt-3.5-turbo",
                "messages": [{"role": "user", "content": resolveResult + question}],
                "temperature": 0.7}
        
        session = Ariadne.service.client_session

        async with session.post(url=url, headers=headers, json=data) as response:
            ret = await response.json()
        status_code = response.status
        if status_code == 200:
            resMes = ret["choices"][0]["message"]["content"]
        else:
            resMes = f"{status_code}, ERROR HASE!"

        return resMes
    
channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, member : Member, message: MessageChain):
    if message.display == "开始连续对话":
        res = oneCont(group, member).start()
        await app.send_message(group,MessageChain([At(member), "\n",res]))

    if message.display[0:4] == "aic ":
        res = await oneCont(group, member).liaotian(message.display[4:])
        await app.send_message(group,MessageChain([At(member), "\n",res]))
