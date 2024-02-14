## 部署方法
### Git克隆仓库
git的基础用法详见[廖雪峰老师的教程](https://www.liaoxuefeng.com/wiki/896043488029600/896067074338496)
```bash
git clone git@github.com:pignoi/mirai-selfbot.git
```
### python环境安装
```bash
conda create -n <your_name> python=3.8
conda activate <your_name>
pip install -r requirements.txt
```
### mirai环境配置
**由于mirai现在支持的手段相对较为复杂（overflow+openshamrock），对服务器有虚拟化要求或者有闲置的Android手机，因此作者已经放弃本项目的继续开发和维护，转战TG吧孩子，人家api甚至有官方文档xD**
参考TBC<br>
要求的拓展：[mirai](https://github.com/mamoe/mirai)   [mirai-api-http](https://github.com/project-mirai/mirai-api-http)

## 相关基础设置
初次启动`main.py`之前，需要编辑`setting-init.json`，其说明如下：
```json
{
    "api-http":{
        "HttpConfig":"",      // 你的mirai-api-http设置中http的地址
        "WebsocketConfig":"",    // 你的mirai-api-http设置中websocket的地址
        "password":""    // 你的mirai-api-http设置中websocket的秘钥
    },
    "user":{
        "qqnumber":[114514],    // mirai机器人的qq号，不要以字符形式填写
        "manageqq":[1919810]    // 作为管理员的qq号，可以设置成大号
    }
}
```
如果想使用openai api相关模块，需要设置环境变量。
```bash
echo export GPT_KEY="xxx" >> ~/.bashrc
bash
```

## 2023.3.12 更新日志
- 增加了openai api部分的异步操作，使之在等待回复的过程中仍然能处理其他信息。
- 增加了日志功能，我们再也不用登陆服务器再看报错啦！
- 增加了README.md
