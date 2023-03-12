import pkgutil

from creart import create
from graia.ariadne.app import Ariadne
from graia.ariadne.connection.config import (
    HttpClientConfig,
    WebsocketClientConfig,
    config,
)
from graia.broadcast import Broadcast
from graia.saya import Saya

from loguru import logger
logger.add("output.log")

saya = create(Saya)

app = Ariadne(
    connection=config(
        1978796129,  # 你的机器人的 qq 号
        "301532aa",  # 填入你的 mirai-api-http 配置中的 verifyKey
        # 以下两行（不含注释）里的 host 参数的地址
        # 是你的 mirai-api-http 地址中的地址与端口
        # 他们默认为 "http://localhost:8080"
        # 如果你 mirai-api-http 的地址与端口也是 localhost:8080
        # 就可以删掉这两行，否则需要修改为 mirai-api-http 的地址与端口
        HttpClientConfig(host="http://localhost:18887"),
        WebsocketClientConfig(host="http://localhost:18887"),
    ),
)

with saya.module_context():
    for module_info in pkgutil.iter_modules(["modules"]):
        saya.require(f"modules.{module_info.name}")
        saya.require(f"modules.arkCard.doRandom")
        saya.require(f"modules.arkCard.localmain")

        saya.require(f"modules.monitor.mm")

app.launch_blocking()
