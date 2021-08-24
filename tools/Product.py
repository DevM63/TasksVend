from . import database, site, user, random
from discord_webhook import DiscordWebhook, DiscordEmbed
import uuid
class Product:

    def id(self, name):
        products = database.select("product", name=name)
        if len(products) == 0: return 0
        else: return products[0][1]
    def getAllStock(self, id: int, day: int):
        stocks = database.select("stock", id=id, day=day)
        return stocks
    def getStock(self, id: int, day: int, amount: int):
        stocks = self.getAllStock(id,day)
        name = self.name(id)
        
        
        l = database.select("label", site=site.id, id=id, day=str(day))[0][3]
        try:
            webhook = DiscordWebhook(url=site.webhook, username="Tasks Team")
            embed = DiscordEmbed(description=f'{user.id}님! 구매 감사합니다. [ {self.name(int(id))} ] ({l} | {amount}개)', color=0xDDDDDD)
            embed.set_footer(text='Tasks Team')
            embed.set_timestamp()
            webhook.add_embed(embed)
            response = webhook.execute()
        except: pass
        idid = str(uuid.uuid4())
        for i in range(amount):
            print(str(stocks[i][2]))
            
            database.insert("raw", id=idid, context=str(stocks[i][2]))
            database.delete("stock", id=id, stock=stocks[i][2], day=day)
        
        database.insert("codelog", sites=site.id, code=f"https://raw.taskv.xyz/{idid}", name=f"{name} [{l}] [{amount}개]", id=user.id)
        database.insert("buylog", sites=site.id, name=f"{name} [{l}] [{amount}개]", id=user.id)
        return f"https://raw.taskv.xyz/{idid}"
    def updateLabel(self, value: str,id:int, day: int):
        print(value, id,day)
        database.update("label", "value", value, site=site.id, id=id, day=day)

    def delStock(self, id:int, value: str, day: int):
        database.delete("stock", id=id, day=day, stock=value)
    def delAllStock(self, id:int, day: int):
        database.delete("stock", id=id , day=day)
    def remove(self, id: int):
        database.delete("stock", id=id)
        database.delete("product", id=id)
        database.delete("price", product_id=id)
    def create(self):
        name = str(random.genVerify())
        database.insert("product", site=site.id, name=name, image="https://cdn.discordapp.com/attachments/797818626656698378/799243455964250112/unknown.png")
        id = self.id(name)
        database.insert("price", sites=site.id, product_id=id, day="1", rank="비구매자", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="7", rank="비구매자", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="30", rank="비구매자", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="1", rank="구매자", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="7", rank="구매자", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="30", rank="구매자", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="1", rank="VIP", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="7", rank="VIP", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="30", rank="VIP", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="1", rank="리셀러", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="7", rank="리셀러", amount=0)
        database.insert("price", sites=site.id, product_id=id, day="30", rank="리셀러", amount=0)
        database.insert("label", site=site.id, id=id, day="1", value="1일")
        database.insert("label", site=site.id, id=id, day="7", value="7일")
        database.insert("label", site=site.id, id=id, day="30", value="30일")
        return name
    def addStock(self, id, day, value):
        database.insert("stock", sites=site.id, id=id, stock=value, day=day)
        


    def name(self, id: int):
        return database.select("product", id=id)[0][2]
    @property
    def category(self):
        category = database.select("category", site=site.id)
        _category = []
        for i in category:
            l = len(database.select("product", site=site.id, category=i[1]))
            _category.append( [ i[1], i[2], l ] )
        return _category
    def productLists(self,category):
        _product = database.select("product", site=site.id, category=category)
        product = []
        for i in _product:
            i1 = database.select("price", sites=site.id, product_id=i[1], rank=user.rank, day="1")
            i7 = database.select("price", sites=site.id, product_id=i[1], rank=user.rank, day="7")
            i30 = database.select("price", sites=site.id, product_id=i[1], rank=user.rank, day="30")

            l1 = database.select("label", site=site.id, id=i[1], day="1")
            l7 = database.select("label", site=site.id, id=i[1], day="7")
            l30 = database.select("label", site=site.id, id=i[1], day="30")
            
            len1 = len(database.select("stock", id=i[1], day="1"))
            len7 = len(database.select("stock", id=i[1], day="7"))
            len30 = len(database.select("stock", id=i[1], day="30"))

            if i[4] == None:
                l = "미분류"
            else:
                l = database.select("category", id=i[4])[0][2]
            product.append([ i[1], i[2], i[3], i1[0][4], i7[0][4], i30[0][4], l1[0][3],l7[0][3],l30[0][3],len1,len7,len30, i[5] ,l])
        return product
    @property
    def productList(self):
        _product = database.select("product", site=site.id)
        product = []
        for i in _product:
            i1 = database.select("price", sites=site.id, product_id=i[1], rank=user.rank, day="1")
            i7 = database.select("price", sites=site.id, product_id=i[1], rank=user.rank, day="7")
            i30 = database.select("price", sites=site.id, product_id=i[1], rank=user.rank, day="30")

            l1 = database.select("label", site=site.id, id=i[1], day="1")
            l7 = database.select("label", site=site.id, id=i[1], day="7")
            l30 = database.select("label", site=site.id, id=i[1], day="30")
            
            len1 = len(database.select("stock", id=i[1], day="1"))
            len7 = len(database.select("stock", id=i[1], day="7"))
            len30 = len(database.select("stock", id=i[1], day="30"))
            if i[4] == None:
                l = "미분류"
            else:
                l = database.select("category", id=i[4])[0][2]
            product.append([i[1], i[2], i[3], i1[0][4], i7[0][4], i30[0][4], l1[0][3],l7[0][3],l30[0][3],len1,len7,len30, i[5],l])
        return product

    def getProduct(self, id):
        s = {
            'main': database.select("product", site=site.id, id=id)[0],
            '비구매자1': database.select("price", sites=site.id, product_id=id, day="1", rank="비구매자")[0],
            '비구매자7': database.select("price", sites=site.id, product_id=id, day="7", rank="비구매자")[0],
            '비구매자30': database.select("price", sites=site.id, product_id=id, day="30", rank="비구매자")[0],

            '구매자1': database.select("price", sites=site.id, product_id=id, day="1", rank="구매자")[0],
            '구매자7': database.select("price", sites=site.id, product_id=id, day="7", rank="구매자")[0],
            '구매자30': database.select("price", sites=site.id, product_id=id, day="30", rank="구매자")[0],

            'VIP1': database.select("price", sites=site.id, product_id=id, day="1", rank="VIP")[0],
            'VIP7': database.select("price", sites=site.id, product_id=id, day="7", rank="VIP")[0],
            'VIP30': database.select("price", sites=site.id, product_id=id, day="30", rank="VIP")[0],

            '리셀러1': database.select("price", sites=site.id, product_id=id, day="1", rank="리셀러")[0],
            '리셀러7': database.select("price", sites=site.id, product_id=id, day="7", rank="리셀러")[0],
            '리셀러30': database.select("price", sites=site.id, product_id=id, day="30", rank="리셀러")[0],

            '라벨30': database.select("label", site=site.id, id=id, day="30")[0],
            '라벨7': database.select("label", site=site.id, id=id, day="7")[0],
            '라벨1': database.select("label", site=site.id, id=id, day="1")[0],
        }
        return s

    @property
    def buylog(self):
        return database.select("buylog", sites=site.id)
    
    @property
    def codelog(self):
        return database.select("codelog", sites=site.id, id=user.id)
    
    
    
    def getPrice(self, id: int, day: int):
        price = database.select("price", product_id=id, day=day, rank=user.rank)
        if len(price) == 0:
            return None
        return price[0][4]
    def updateName(self, id: int, value):
        database.update("product", "name", value, id=id)
    def updateImage(self, id: int, value):
        database.update("product", "image", value, id=id)
    def updatePrice(self, id: int, day: int, rank: str, value: int):
        database.update("price", "amount", value, product_id=id, day=day, rank=rank)
        
    def delete(self, id: int):
        database.delete("product", id=id)
product = Product()
