from tools import database, random

c = int(input("How Much: "))
d = int(input("Day: "))

for i in range(c):
    code = random.genToken(7)
    database.insert("license", code=code, day=d)
    print(f"[{d}Day] Code: {code}")