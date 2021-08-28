import os, time
import requests
from tools import database

class VkrCulture:
    def __init__(self) -> None: pass
    def charge(self, id, pw, pin):
        res = requests.post("http://ultra0221.mcgo.kr/charge", json={
            "api_key": "PUT_API_KEY_HERE",
            "cid": id,
            "cpw": pw,
            "pin": pin,
        })
        obj = res.json()
        return VkrResult(self, id, obj["success"], obj["amount"], obj["result"], obj["time"])

class VkrResult:
    def __init__(self, obj: VkrCulture, cid: str, success: bool, amount: int, result: str, time: int):
        self.__obj: VkrCulture = obj
        self.culture_id: str = cid
        self.success: bool = success
        self.amount: int = amount
        self.msg: str = result
        self.time: int = time
    def __repr__(self) -> str:
        return f"<VkrResult culture_id=\"{self.culture_id}\" success={self.success} amount={self.amount} msg=\"{self.msg}\" time={self.time}>"

vkrobj = VkrCulture()

def CulturelandAutoCharge(id, pw, code):
    result = vkrobj.charge(id, pw, code)
    return (result.amount, result.msg)
