from graia.ariadne.message.element import Image as mImage
from graia.ariadne.app import Ariadne
from graia.ariadne.event.message import FriendMessage
from graia.ariadne.message.chain import MessageChain
from graia.ariadne.model import Friend

from graia.saya import Channel
from graia.saya.builtins.broadcast.schema import ListenerSchema

from PIL import Image, ImageFont, ImageDraw
from io import BytesIO

from loadJson import loadJson

channel = Channel.current()
managers = loadJson().getManage()

def getOHlog(num):
    num = int(num)
    with open("./output.log") as f:
        resMes = f.readlines()[-1:-num:-1][::-1]
    text = "".join(resMes)
    im = Image.new("RGB", (1200, 15*num), (255, 255, 255))
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype("./fonts/Courier.ttc", 12)
    
    dr.text((10, 5), text, font=font, fill="#000000")
    new_img = im.convert("RGB")
    img_byte = BytesIO()
    new_img.save(img_byte, format='PNG') # format: PNG or JPEG
    binary_content = img_byte.getvalue()  # im对象转为二进制流
    
    return binary_content

@channel.use(ListenerSchema(listening_events=[FriendMessage]))
async def setu(app: Ariadne, friend: Friend, message: MessageChain):
    if (friend.id in managers) and message.display[0:2] == "日志":
        imbytes = getOHlog(message.display[3:])

        await app.send_message(friend, MessageChain(
                        mImage(data_bytes=imbytes)
                        ))
            
    else:
        return 

