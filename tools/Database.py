import pymysql

class Database:


    def get(self):
        conn = pymysql.connect(
                user='root', 
                passwd='DBPASSWORD', 
                host='127.0.0.1', 
                db='tasks', 
                charset='utf8'
            )
        cur = conn.cursor()
        return conn, cur
    def update(self, table: str, _name_: str, _value_, **args):
        conn, cur = self.get()
        sql = f"UPDATE {table} SET {_name_} = %s WHERE "
        c = 1
        keys = args.keys()
        for i in keys:
            if len(keys) == c:
                sql += i + "=%s "
            else:
                sql += i + "=%s and "
            c += 1
        x = [_value_]
        x.extend(args.values())
        cur.execute(sql, x)
        conn.commit()
        conn.close()
    def delete(self, table: str, **args):
        conn, cur = self.get()
        sql = "DELETE FROM " +  table + " WHERE "
        c = 1
        keys = args.keys()
        for i in keys:
            if len(keys) == c:
                sql += i + "=%s "
            else:
                sql += i + "=%s and "
            c += 1
        cur.execute(sql, tuple(args.values()))
        conn.commit()
        conn.close()
    def select(self, table: str, **args):
        conn, cur = self.get()
        sql = "SELECT * FROM " +  table + " WHERE "
        c = 1
        keys = args.keys()
        for i in keys:
            if len(keys) == c:
                sql += i + "=%s "
            else:
                sql += i + "=%s and "
            c += 1
        cur.execute(sql, tuple(args.values()))
        result = cur.fetchall()
        conn.close()
        return result
    def addStock(self, sites, id, stocks, day):
    #database.insert("stock", sites=site.id, id=id, stock=i, day=day)
        conn, cur = self.get()
        for stock in stocks:
            cur.execute("INSERT INTO stock VALUES(%s,%s,%s,%s)", (sites, id, stock,day,))
        conn.commit()
        conn.close()

    def insert(self, table: str, **args):
        conn, cur = self.get()
        sql = "INSERT INTO " +  table + " ("
        c = 1
        keys = args.keys()
        for i in keys:
            if len(keys) == c:
                sql += i
            else:
                sql += i + ", "
            c += 1
        sql += ") VALUES ("
        c = 1
        _values = args.values()
        for i in _values:
            if len(_values) == c:
                sql += "%s"
            else:
                sql += "%s, "
            c += 1
        sql += ");"
        cur.execute(sql, tuple(_values))
        conn.commit()
        conn.close()
database = Database()
