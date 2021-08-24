from . import random, user, session, site, database

class Coupon:
    def Delete(self,code):
        c = database.select("coupon", sites=site.id, number=code)
        if len(c) == 1:
            database.delete("coupon", sites=site.id, number=code)
            return True
        else:
            return False
    def Gen(self,amount):
        code = random.genCoupon()
        database.insert("coupon", sites=site.id, number=code, amount=amount)
        return code
    def Use(self,code):
        c = database.select("coupon",sites=site.id, number=code)
        if len(c) == 1:
            database.delete("coupon",sites=site.id, number=code)
            user.updateAmount(user.amount + int(c[0][2]))
            return True, int(c[0][2])
        else:
            return False, 0
    @property
    def List(self):
        c = database.select("coupon",sites=site.id)
        return c
coupon = Coupon()