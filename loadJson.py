import json

class loadJson:
    def __init__(self):
        self.jsonFile = json.load(open("setting.json"))

    def allMain(self):
        qqnumber = self.jsonFile["user"]["qqnumber"]
        passwd = self.jsonFile["api-http"]["password"]
        http = self.jsonFile["api-http"]["HttpConfig"]
        websocket = self.jsonFile["api-http"]["WebsocketConfig"]
        
        return [qqnumber, passwd, http, websocket]

    def getManage(self):
        managers = self.jsonFile["user"]["manageqq"]

        return managers