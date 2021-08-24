import random as _random
import string as _string

class Random:
    def genToken(self,i):
        st = ""
        for _ in range(i):
            st += _random.choice(_string.ascii_letters + "0123456789")
        return st
    def genAccount(self):
        st = ""
        for _ in range(6):
            st += _random.choice("가나다라마바사태종태새문단새세총병진병신애로우오얘배니마너나버")
        return st
    def genVerify(self):
        st = ""
        for _ in range(6):
            st += _random.choice("0123456789")
        return st
    def genCoupon(self):
        st = ""
        for _ in range(10):
            st += _random.choice(_string.ascii_letters + "0123456789")
        return st
random = Random()