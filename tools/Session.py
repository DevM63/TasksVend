
from flask import request, session as s

class Session:
    def set(self,name,value):
        s[request.host+"="+name] = value    
    def get(self,name):
        if request.host + '='+ name in s:
            return s[request.host + "=" + name]
        return "None"
session = Session()