from flask import request
from . import database,session
class Site:

    @property
    def id(self):
        sites = database.select("sites", address=request.host)
        
        if len(sites) == 0: return "0"
        return sites[0][0]
    @property
    def template(self):
        sites = database.select("sites", address=request.host)
        if len(sites) == 0: return "v2"
        return sites[0][24]
    def color(self):
        return database.select("sites", id=self.id)[0][20].split("|")
    @property
    def message(self):
        rank = database.select("user", sites=site.id, name=session.get("login"))[0][5]
        if rank == "비구매자":  return database.select("sites", id=self.id)[0][2]
        if rank == "구매자":  return database.select("sites", id=self.id)[0][15]
        if rank == "VIP":  return database.select("sites", id=self.id)[0][16]
        if rank == "리셀러":  return database.select("sites", id=self.id)[0][17]
    @property
    def culture(self):
        return database.select("sites", id=self.id)[0][4]
    @property
    def culturedown(self):
        return database.select("sites", id=self.id)[0][5]
    @property
    def webhook(self):
        return database.select("sites", id=self.id)[0][6]
    @property
    def name(self):
        return database.select("sites", id=self.id)[0][9]
    @property
    def music(self):
        return database.select("sites", id=self.id)[0][21]
    @property
    def bankpin(self):
        return database.select("sites", id=self.id)[0][7]

    @property
    def logo(self):
        return database.select("sites", id=self.id)[0][23]
    
    
    @property
    def buylog(self):
        if database.select("sites", id=self.id)[0][22] == "on": return True
        else: return False
    @property
    def isVerify(self):
        if database.select("sites", id=self.id)[0][10] == "on": return True
        else: return False
    @property
    def bank(self):
        return database.select("sites", id=self.id)[0][3]
    @property
    def cultureapi(self):
        return database.select("sites", id=self.id)[0][8].split(":")

    def setBank(self, value):
        return database.update("sites","account", value, id=self.id)
            

    def setMessage(self, value):
        return database.update("sites","message", value, id=self.id)
            
    def setCulture(self, value):
        return database.update("sites","culture", value, id=self.id)

    def setMusic(self, value):
        return database.update("sites","music", value, id=self.id)          
    def setWebhook(self, value):
        return database.update("sites","discordwebhook", value, id=self.id)
                
    def setCulturedown(self, value: int):
        return database.update("sites","culturedown", value, id=self.id)
        
    def setBuylog(self, value: bool):
        if value: database.update("sites","buylog", "on", id=self.id)
        else: database.update("sites","buylog", "off", id=self.id)

    def setNotice(self, value: str):
        return database.update("sites","message", value, id=self.id)
    def setName(self, value: int):
        return database.update("sites","name", value, id=self.id)
    def setVerfiy(self, value: bool):
        if value: database.update("sites","verify", "on", id=self.id)
        else: database.update("sites","verify", "off", id=self.id)
    def setLogo(self, value: str):
        return database.update("sites","logo", value, id=self.id)
site = Site()
