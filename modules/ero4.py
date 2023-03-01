from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import GroupMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Group

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

import openai

openai.api_key = "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"
def askChatGPT(question):
    prompt = question

    completions = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text
    return message

channel = Channel.current()

@channel.use(ListenerSchema(listening_events=[GroupMessage]))
async def setu(app: Ariadne, group: Group, message: MessageChain):
    if message.display[0:3] == "ai ":
        res = askChatGPT(message.display[3:])
        await app.send_message(
            group,
            MessageChain(f"{res[2:]}"),
         )
    else:
        return 