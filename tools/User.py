from . import session, random, database, site
import hashlib
from flask import request
class User:
    
    def create(self):
        
        account = random.genAccount()
        database.insert(
            "user", 
            sites=site.id,
            name=self.id, 
            pw=self.password,
            number=self.number,
            money=0, 
            rank="비구매자", 
            bankname=account,
            refer_by=session.get("refer_code")
        )
        session.set("login", self.id)
    @property
    def id(self):
        username = session.get("register=username")
        if username != "None": return username
        return session.get("login")

    @property
    def rank(self):
        return database.select("user", sites=site.id, name=self.id)[0][5]

     
    
    def updateAmount(self, amount: int, id=None):
        if id == None:
            id = self.id
        account = random.genAccount()
        database.update("user", "money", amount, sites=site.id, name=id)

    @property
    def bank(self):
        return database.select("user", sites=site.id, name=self.id)[0][6]


        
    def updateRank(self, rank: str, id=None):
        if id == None:
            id = self.id
        account = random.genAccount()
        database.update("user", "rank", rank, sites=site.id, name=id)
    def getIP(self):
        ip = request.headers.get('CF-Connecting-IP')
        if ip == None:  
            ip = request.remote_addr
        return ip
    def login(self):
        session.set("login", self.id)
    
    @property
    def password(self):
        user = database.select("user", sites=site.id, name=self.id)
        if len(user) ==  1: return user[0][2]
        
        return session.get("register=password")

    def isUser(self,id):
        user = database.select("user", sites=site.id, name=id)
        if len(user) ==  1: return True
        return False

    @property
    def number(self):
        return session.get("register=number")

    @property
    def verifyCode(self):
        return session.get("register=code")

    def setVerifyCode(self, code):
        session.set("register=code", code)

    def setNumber(self, number):
        session.set("register=number", number)
    
    @property
    def amount(self):
        return int(database.select("user", sites=site.id, name=self.id)[0][4])

    def setAccount(self, username, password):
        session.set("register=password", password)
        session.set("register=username", username)

    def logout(self):
        session.set("register=password", "None")
        session.set("register=username", "None")
        session.set("register=number", "None")
        session.set("register=code", "None")
        session.set("login", "None")

    def getUser(self, id):
        return database.select("user", sites=site.id, name=id)[0]
    @property
    def usersList(self):
        return database.select("user", sites=site.id)
        
user = User()
