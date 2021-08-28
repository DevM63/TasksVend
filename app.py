import json, sqlite3, os, string, random, hashlib, requests, time, Auto, json, datetime, uuid
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf.csrf import CSRFProtect
from discord_webhook import DiscordWebhook, DiscordEmbed
from flask_wtf import Form, RecaptchaField
from tools import database, PostForm, random, session, site, user as users, product, coupon
from flask_discord import DiscordOAuth2Session, requires_authorization, Unauthorized
def Value():
    # title=site.name, log=product.buylog
    return {
        'color': site.color(),
        'plugins': database.select("sites",id=site.id)[0][18],
        'uid': database.select("user", name=users.id, sites=site.id)[0][7],
        'category': product.category,
        'username': users.id,
        'logo': site.logo,
        'useramount': users.amount,
        'userrank': users.rank,
        'host' : request.host,
        'title': site.name, 
        'pl': len(database.select("product", site=site.id)),
        'notice': site.message,
    }
app = Flask(__name__)
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "true"  
# app.url_map.host_matching = True
app.config["DISCORD_CLIENT_ID"] = 0
app.config["DISCORD_CLIENT_SECRET"] = ""              
app.config["DISCORD_REDIRECT_URI"] = "https://discord.도메인/callback/"           
app.config["DISCORD_BOT_TOKEN"] = ""                
app.config['RECAPTCHA_PUBLIC_KEY']=''
app.config['RECAPTCHA_PRIVATE_KEY']=''
urls = ['create', 'root', 'status','admin', 'raw', 'sms','captcha', 'discord', 'refer']
# urls 에 있는 도메인들 전부 서버로 연결합니다.
n = ["도메인"]
template = [
    ("부트스트랩", "v2"), 
]
for i in urls:
    n.append(f"{i}.{n[0]}")
discord = DiscordOAuth2Session(app)
app.secret_key = ""
class ReCaptcha(Form):
    recaptcha = RecaptchaField()
@app.route("/register", methods=["GET"])
def register_GET():
    if users.id != "None":
        return redirect("/")
    code = request.args.get("refer")
    if code != "" and code != None:
        a = database.select("user",refer_code=code)[0][1]
        session.set("refer_code", a)
    form = PostForm
    return render_template(site.template+"/reg.html",form=form,title=site.name)

@app.route("/register", methods=["POST"])
def register_POST():
    if site.isVerify:
        print(users.id,users.number)
        if users.id != "None":
            if users.number != "None":
                db = database.select("verify", number=users.number, code=users.verifyCode)
                database.delete("verify", number=users.number, code=users.verifyCode)
                if db[0][2] == "y":
                    token = str(uuid.uuid4())
                    database.insert("captcha",address=request.host, token=token)

                    return redirect("https://captcha.도메인/"+token)
                else:
                    users.logout()
                    return redirect("/login")
            else:
                number = request.form.get("number")
                print(number)
                if number.startswith("010"):
                    users.setNumber(number)
                    code = random.genVerify()
                    res = requests.post("http://m63.asuscomm.com:8080/", json={
                        "api_key": "",
                        "number": number,
                    })
                    # 휴대폰 인증 작동 X
                    resjson = res.json()
                    code = resjson["code"]
                    session.set("register=code", code)
                    database.insert("verify", number=number, code=code, isVerify="n")
                    form = PostForm
                    return render_template(site.template+"/smsverifyf.html", form=form, code=code)
                else:
                    users.logout()
                    return render_template(site.template+"/goto.html",message="010 전화번호만 인증이 가능합니다.", url="/register") 
        username = request.form.get("username")
        if users.isUser(username):
            users.logout()
            return render_template(site.template+"/goto.html",message="이미 존재하는 유저입니다.", url="/register") 
        else:
            if (username == None or username == "None" or username == ""):
                code = request.args.get("refer")
                if code != "" and code != None:
                    a = database.select("user",refer_code=code)[0][1]
                    session.set("refer_code", a)
                form = PostForm
                return render_template(site.template+"/reg.html",form=form)

            if users.id == 'None':
                i1 = hashlib.sha3_512(request.form.get("pass", "").encode()).hexdigest()
                passwd = hashlib.sha3_512(i1.encode()).hexdigest()
                print(username,passwd)
                users.setAccount(username, passwd)
            form = PostForm
            return render_template(site.template+"/smsverify.html",form=form)

    else:
        username = request.form.get("username")
        if users.isUser(username):
            users.logout()
            return render_template(site.template+"/goto.html",message="이미 존재하는 유저입니다.", url="/register")               
        i1 = hashlib.sha3_512(request.form.get("pass", "").encode()).hexdigest()
        passwd = hashlib.sha3_512(i1.encode()).hexdigest()
        users.setAccount(username, passwd)
        token = str(uuid.uuid4())
        database.insert("captcha",address=request.host, token=token)

        return redirect("https://captcha.도메인/"+token)
        # /auth/<token>
@app.route("/captcha/<token>", methods=["POST"])
def captcha_end(token):
    if site.id == "0":
       
        return redirect("/404")
    else:
            
        _auth = database.select("captcha", token=token)
        if len(_auth) == 1:
            SECRET_KEY = ""   
            hcaptcha = request.form.get('h-captcha-response')
            VERIFY_URL = "https://hcaptcha.com/siteverify"
            session.set("captcha", "None")
            res = requests.post(VERIFY_URL, data={'secret': SECRET_KEY, 'response': hcaptcha})
            success = res.json()['success']
            database.delete("captcha", token=token)
            
            if success:
                users.create()
                try:
                    a = int(database.select("user", sites=site.id, name=session.get("refer_code"))[0][10]) + 1
                    database.update("user", "refer_count", a, sites=site.id,name=session.get("refer_code"))
                except:
                    pass
                users.login()
                return redirect("/")
            else:
                users.logout()
                return redirect(f"/register")
            
        else:
            return render_template(site.template+"/goto.html",message="잘못 된 요청입니다.", url="https://discord.gg/3qy7eBTXRS") 

@app.route("/<token>", methods = ["GET" , "POST"])
def root(token):
    if request.path == "/404":
        return render_template(site.template+"/404.html")
    elif request.host == "도메인":
        if token == "sms":
            obj = request.get_json()
            number = obj["title"]
            code = obj["code"]
            l = database.select("verify", number=number, code=code)
            if len(l):
                database.update("verify", "isVerify", "y", number=number, code=code)

        return redirect(f"https://{token}.도메인")


    elif request.host == "refer.도메인":
        _auth = database.select("user", refer_code=token)
        if len(_auth) == 1:
            site_id = _auth[0][0]
            sites = database.select("sites", id=site_id)[0]
            return redirect(f"https://{sites[1]}/register?refer="+token)
        else:
            return render_template(site.template+"/goto.html",message="잘못 된 요청입니다.", url="https://discord.gg/3qy7eBTXRS") 
    elif request.host == "discord.도메인":
        _auth = database.select("auth", token=token)
        if len(_auth) == 1:
            session.set("auth", token)
            return discord.create_session(scope=["identify"])
        else:
            return render_template(site.template+"/goto.html",message="잘못 된 요청입니다.", url="https://discord.gg/3qy7eBTXRS")    
    elif request.host == "captcha.도메인":
        _auth = database.select("captcha", token=token)
        if len(_auth) == 1:
            address = _auth[0][0]
            session.set("captcha", token)
            return render_template(site.template+"/captcha.html",address=address,token=token)
        else:
            return render_template(site.template+"/goto.html",message="잘못 된 요청입니다.", url="https://discord.gg/3qy7eBTXRS")    

    elif request.host == "raw.도메인":
        _auth = database.select("raw", id=token)
        return render_template(site.template+"/raw.html",raw=_auth)
    return redirect("/404")

@app.route("/callback/")
def callback():
    discord.callback()
    return redirect("/auth/end")
@app.route("/auth/end")
@requires_authorization
def end():
    if request.host == "discord.도메인":
        
        token = session.get("auth")
        _auth = database.select("auth", token=token)
        if len(_auth) == 1:
            session.set("auth", "None")
            _user = discord.fetch_user()
            id = _user.id
            suser = _auth[0][2]
            address = _auth[0][0]
            a = database.select("sites", address=address)[0]
            
            print(a[0], suser)
            database.update("user", "did", str(id), name=str(suser),sites=str(a[0]) )
            database.delete("auth", token=token)
            discord.revoke()
            session.set("auth_address", address)
            return render_template(site.template+"/goto.html",message="성공적으로 연동 되었습니다.", url="https://"+address)     
            
        else:
            discord.revoke()
            return render_template(site.template+"/goto.html",message="잘못 된 요청입니다.", url="https://discord.gg/3qy7eBTXRS")     
@app.errorhandler(Unauthorized)
def redirect_unauthorized(e):
    return redirect("/auth/"+session.get("auth"))  
@app.before_request
def before_request():
    if not request.host.endswith("도메인"):
        return "404 not found"
    if not request.host in n:
        # print("REQUEST",request.host)
        # requests.post("http://localhost:5000/log", data={'ip': request.headers['CF-Connecting-IP'], 'url': request.url, 'methods':request.method})
        _site = database.select("sites", id=site.id)
        a = _site[0][12].split(" ")[0].split("-")
        now = datetime.datetime.now()
        old = now.replace(year=int(a[0]), month=int(a[1]), day=int(a[2]))
        if (now.year == old.year) and now.month > old.month or (now.year > old.year) or (now.year == old.year and now.month == old.month and now.day > old.day):
            if request.path == "/exp":
                if request.method.upper() == "GET":
                    return render_template(site.template+"/se.html")
                value = request.form.get("value")
                license_key = database.select("license", code=value)
                if len(license_key) == 0:
                    return render_template(site.template+"/goto.html",message="잘못된 라이센스 코드 입니다.", url="/")
                s = database.select("sites", id=site.id)[0]
                a = s[12].split(" ")[0].split("-")
                now = datetime.datetime.now()
                    
                database.delete("license", code=value)
                now = datetime.datetime.now()
                now = now  + datetime.timedelta(days=license_key[0][1])
                st = str(now.astimezone())
                database.update("sites", "end", st, address=request.host)
                return render_template(site.template+"/goto.html",message="사이트가 연장되었습니다.", url="/")
            else:
                return render_template(site.template+"/se.html")

            

        if users.isUser(users.id):
            
            ip = request.headers.get("CF-Connecting-IP")
            dbdb = database.select("visitlog", sites=site.id,id=users.id, ip=ip)
            isBaned = len(database.select("visitlog", sites=site.id,ip=ip, isban="true"))
            if isBaned != 0:
                if len( dbdb) == 0:
                    database.insert("visitlog", sites=site.id, id=users.id, ip=ip, isban="true")
                
                return "사이트 관리자에게 문의 해주세요. (B)"
            if len( dbdb) == 0:
                database.insert("visitlog", sites=site.id, id=users.id, ip=ip, isban="false")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/login")
@app.route("/login", methods=["GET"])
def login_GET():
    if users.id != "None":
        return redirect("/")
    form = PostForm
    return render_template(site.template+"/login.html",form=form,title=site.name)
@app.route("/login", methods=["POST"])
def login_POST():
    username = request.form.get("username")
    i1 = hashlib.sha3_512(request.form.get("pass").encode()).hexdigest()
    passwd = hashlib.sha3_512(i1.encode()).hexdigest()
    users.setAccount(username,passwd)
    if username.isalnum() == False:
        return redirect("/login")
    elif username.isalnum() == True:
        if users.isUser(username):
            password = database.select("user", sites=site.id, name=users.id)[0][2]
            if str(password) == passwd:
                
                users.login()
                return redirect("/")

            users.logout()
            return render_template(site.template+"/goto.html",message="아이디 또는 비밀번호가 일치 하지 않습니다.", url="/login")
        else:
            users.logout()
            return render_template(site.template+"/goto.html",message="아이디 또는 비밀번호가 일치 하지 않습니다.", url="/login")
@app.route("/", methods=["GET", "POST"])
def index():
    if request.host == "도메인":
        return redirect("https://discord.gg/3qy7eBTXRS")
    if request.host == "create.도메인":
        if request.method == "GET":
            return render_template(site.template+"/sitec.html")
        if request.method == "POST":
            license_code = request.form.get("code")
            license_key = database.select("license", code=license_code)
            if len(license_key) == 1:
                address = request.form.get("address","No Address")
                name = request.form.get("name","No Name")
                if address == "No Address" or address.strip() == "" or name == "No Name" or name.strip() == "":
                    return render_template(site.template+"/goto.html",message="빈칸은 허용되지 않습니다.", url="/")
                if address.isalnum() == False:
                    return render_template(site.template+"/goto.html", message="사이트 주소에는 특수문자가 들어갈 수 없습니다.")
                if address in urls:
                    return render_template(site.template+"/goto.html", message="허용되지 않는 주소 입니다.")
                _site = database.select("sites", address=address+".도메인")
                if len(_site) == 0:
                    createCloudflare(address)
                    now = datetime.datetime.now() + datetime.timedelta(days=license_key[0][1])
                    st = str(now.astimezone())
                    database.delete("license", code=license_code)
                    conn, cur = database.get()
                    cur.execute(
                    "INSERT INTO sites VALUES(NULL,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,NULL,NULL,NULL,NULL,NULL,NULL,0, %s, NULL, NULL,NULL, %s)",
                    (address+".도메인","Free Vend!.", "null", "", 0, "", "", "", name, "off", str(users.id), st,"4e4e50|1a1a1d|fff|2c2c2e|fff|1a1a1d|fff|fff|gray|fff|302f2f","v2",)
                    )

                    conn.close()
                    #database.insert("sites",address=address+".도메인",cultureapi=c, name=name, by=str(users.id),end=st)
                    return render_template(site.template+"/goto.html",message="사이트 생성되었습니다. (가입아이디: Master)", url="https://"+address+".도메인")
                else:
                    return render_template(site.template+"/goto.html",message="현재 해당 주소는 사용중입니다.", url="/")
                # else:
                #     
            else:
                return render_template(site.template+"/goto.html",message="잘못된 라이센스 코드 입니다.", url="/")

    if site.id == "0":
       
        return redirect("/404")
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            
            return render_template(site.template+"/index.html", **Value(), tab="메인")
@app.route("/setting/normal/addLicense", methods=["POST"])
def setting_normal_addLicense():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                license_key = database.select("license", code=value)
                if len(license_key) == 0:
                    return render_template(site.template+"/goto.html",message="잘못된 라이센스 코드 입니다.", url="/setting/normal")
                s = database.select("sites", id=site.id)[0]
                a = s[12].split(" ")[0].split("-")
                now = datetime.datetime.now()
                
                database.delete("license", code=value)
                now = datetime.datetime.now()
                now = now.replace(year=int(a[0]), month=int(a[1]), day=int(a[2]))
                now = now  + datetime.timedelta(days=license_key[0][1])
                st = str(now.astimezone())
                database.update("sites", "end", st, address=request.host)
                return render_template(site.template+"/goto.html",message="사이트가 연장되었습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
 
@app.route("/calc", methods=["GET", "POST"])
def calc():
    if site.id == "0":
       
        return redirect("/404")
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            a = request.host
            if a == "xoupon.도메인":
                return render_template(site.template+"/goto.html",message="Xonpon 은 컬쳐랜드 수수료 계산기를 지원하지 않습니다.", url="/")
            else:
                return render_template(site.template+"/calc.html", culturedown=site.culturedown)

@app.route("/setting/gift/delete/<code>")
def setting_gift_delete(code):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                coupon.Delete(code)
                return render_template(site.template+"/goto.html",message="기프트 삭제 완료", url="/setting/gift")
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/gift", methods=["GET"])
def setting_gift():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                return render_template(site.template+"/setting_gift.html",**Value(), list=coupon.List)
            else:
                return render_template(site.template+"/404.html"), 404
@app.route('/setting/gift/gen', methods=["POST"])
def giftgen():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                amount = request.form.get("amount")
                code = coupon.Gen(amount)
                return render_template(site.template+"/goto.html",message=f"기프트 발급완료 (코드: {code})", url="/setting/gift")
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/connect/discord", methods=["GET", "POST"])
def connectDiscord():
    if site.id == "0":
        return redirect("/404")
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            _user = database.select("user", sites=site.id, name=users.id)[0]
            if _user[7] == None:
                token = str(uuid.uuid4())
                database.insert("auth", address=request.host, token=token, user=users.id)
                return redirect("https://discord.도메인/"+token)
            else:
                return render_template(site.template+"/goto.html",message="이미 연동을 하셨습니다.", url="/")
            



@app.route("/buylog", methods=["GET", "POST"])
def buylog():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            a = request.host
            if a == "xoupon.도메인":
                return render_template(site.template+"/goto.html",message="Xonpon 의 구매로그는 비공개 입니다.", url="/")
            if a == "hazard.도메인":
                return render_template(site.template+"/goto.html",message="Hazard 의 구매로그는 비공개 입니다.", url="/")
            else:
                return render_template(site.template+"/buylog.html",**Value(),log=product.buylog)


            
@app.route("/codelog", methods=["GET", "POST"])
def codelog():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            return render_template(site.template+"/codelog.html", **Value(), log=product.codelog)


@app.route("/list/<int:id>", methods=["GET", "POST"])
def __list(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            return render_template(site.template+"/list.html", productList=product.productLists(id),**Value())


@app.route("/list", methods=["GET", "POST"])
def _list():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            return render_template(site.template+"/list.html",productList=product.productList, **Value())
@app.route("/charge/bank", methods=["GET", "POST"])
def charge_bank():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            return render_template(site.template+"/bank.html", **Value(), bankname=users.bank , bankaccount=site.bank, tab="계좌 충전")
@app.route("/redeem", methods=["POST"])
def redeem():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            code = request.form.get("code")
            result, amount = coupon.Use(code)
            if result: return {"success": True, "amount": amount}
            else: return {"success": False, "message": "'알 수 없는 기프트 카드 코드 입니다.'"}
@app.route("/redeem", methods=["GET"])
def redeem_GET():
    if site.id == "0": return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None": return redirect("/login")
        else:
            return render_template(site.template+"/redeem.html", **Value())
@app.route("/refer", methods=["GET", "POST"])
def _refer():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            user = database.select("user", name=users.id, sites=site.id)
            refer = user[0][8]
            if refer == None or refer == "None" or refer == "": 
                refer = str(random.genVerify())
                database.update("user", "refer_code",refer,sites=site.id, name=users.id)
            refer_pencent = database.select("sites", id=site.id)[0][19]
            return render_template(site.template+"/refer.html", refer=refer, refer_pencent=refer_pencent,**Value(), tab="내 추천인")
@app.route("/charge/culture", methods=["GET", "POST"])
def charge_culture():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            a = request.host

            return render_template(site.template+"/culture.html", **Value(), tab="문화상품권")
            

@app.route("/setting/ip", methods=["GET", "POST"])
def setting_ip():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                return render_template(site.template+"/setting_ip.html",**Value(), site=site.id,ips=database.select("visitlog", sites=site.id))
            else:
                return render_template(site.template+"/404.html"), 404
                
@app.route("/setting/ip/<ip>", methods=["POST"])
def setting_ban(ip):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                isBan = request.form.get("value")
                database.update("visitlog", "isban", isBan, ip=ip)
                return redirect("/setting/ip")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/normal", methods=["GET", "POST"])
def setting_normal():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                s = database.select("sites", id=site.id)[0]
                refer_percent = s[19]
                end = s[12].split(" ")[0]

                gid = str(s[13])
                rid = str(s[14])
                notice1 = database.select("sites", id=site.id)[0][2]
                notice2 = database.select("sites", id=site.id)[0][15]
                notice3 = database.select("sites", id=site.id)[0][16]
                notice4 = database.select("sites", id=site.id)[0][17]
                print(site.color())
                return render_template(site.template+"/setting_normal.html",**Value(),t=template,tt=site.template, refer_percent=refer_percent, gid=gid, rid=rid,webhook=site.webhook,notice1=notice1, notice2=notice2, notice3=notice3, notice4=notice4, logo_url=site.logo, end=end)
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/normal/editLayout", methods=["POST"])
def setting_normal_editLayout():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                database.update("sites", "template", value,id=site.id)
                return render_template(site.template+"/goto.html",message="레이아웃 완료", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/user/createform", methods=["GET"])
def setting_userCreateForm():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                
                return render_template(site.template+"/create_user.html")
            else:
                return render_template(site.template+"/404.html"), 404
 

@app.route("/setting/user/create", methods=["POST"])
def setting_userCreate():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                username = request.form.get("username")
                i1 = hashlib.sha3_512(request.form.get("pass", "").encode()).hexdigest()
                passwd = hashlib.sha3_512(i1.encode()).hexdigest()
                print(username,passwd)
                users.setAccount(username, passwd)
                return render_template(site.template+"/goto.html",message="성공적으로 유저를 생성했습니다.", url="/setting/users")
            else:
                return render_template(site.template+"/404.html"), 404
 


@app.route("/setting/normal/editBuylog", methods=["POST"])
def setting_normal_editBuylog():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                if value == "on": site.setBuylog(True)
                else: site.setBuylog(False)
                return render_template(site.template+"/goto.html",message="성공적으로 설정했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/normal/editLogo", methods=["POST"])
def setting_normal_editLogo():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                site.setLogo(value)
                return render_template(site.template+"/goto.html",message="성공적으로 설정했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404


@app.route("/setting/normal/editVerify", methods=["POST"])
def setting_normal_editVerify():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                if value == "on": site.setVerfiy(True)
                else: site.setVerfiy(False)
                return render_template(site.template+"/goto.html",message="성공적으로 설정했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
 

@app.route("/setting/normal/editRole", methods=["POST"])
def setting_normal_editRole():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                database.update("sites", "role", value, id=site.id)
                return render_template(site.template+"/goto.html",message="성공적으로 설정했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/normal/editChannelTalk", methods=["POST"])
def setting_normal_editChannelTalk():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                database.update("sites", "channelplugin", value, id=site.id)
                return render_template(site.template+"/goto.html",message="성공적으로 채널톡이 설정했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/normal/editColor", methods=["POST"])
def setting_normal_editColor():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                sidebar = request.form.get("sidebar")
                sidebar_text = request.form.get("sidebar_text")

                box = request.form.get("box")
                box_text = request.form.get("box_text")

                pbox = request.form.get("pbox")
                pbox_text = request.form.get("pbox_text")

                pbol = request.form.get("pbol")
                pbol_text = request.form.get("pbol_text")
                
                pbtn = request.form.get("pbtn")
                pbtn_text = request.form.get("pbtn_text")

                background = request.form.get("background")
                sidebar_hover = request.form.get("sidebar_hover")
                database.update("sites", "color",f"{background}|{sidebar}|{sidebar_text}|{box}|{box_text}|{pbox}|{pbox_text}|{pbol}|{pbtn}|{pbtn_text}|{sidebar_hover}", id=site.id)
                return render_template(site.template+"/goto.html",message="성공적으로이 색을 설정했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/normal/editNotice/<int:id>", methods=["POST"])
def setting_normal_editNotice(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                if id == 1: database.update("sites","message", value, id=site.id)
                elif id == 2: database.update("sites","message2", value, id=site.id)
                elif id == 3: database.update("sites","message3", value, id=site.id)
                elif id == 4: database.update("sites","message4", value, id=site.id)
                return render_template(site.template+"/goto.html",message="공지 변경 완료", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/normal/editAccount", methods=["POST"])
def setting_normal_editaccount():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                if value.strip() == "" or value == None:
                    return render_template(site.template+"/goto.html",message="공백또는 빈 계좌 정보는 허용하지 않습니다. 계좌 비활성화는 null 로 설정해주시면 됩니다.", url="/setting/normal")
                site.setBank(value)
                return render_template(site.template+"/goto.html",message="성공적으로 계좌 정보를 변경했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
# @app.route("/setting/normal/deleteCulture", methods=["POST"])
# def setting_normal_deleteCulture():
#     if site.id == "0":
#         return render_template(site.template+"/404.html"), 404
#     else:
#         if users.id == "None":
#             return redirect("/login")
#         else:
#             if users.id == "Master":
#                 value = request.form.get("value")
#                 culture.delete(value)
#                 return render_template(site.template+"/goto.html",message="성공적으로 컬쳐랜드 계정을 삭제했습니다.", url="/setting/normal")
#             else:
#                 return render_template(site.template+"/404.html"), 404
# @app.route("/setting/normal/editCulture", methods=["POST"])
# def setting_normal_editCulture():
#     if site.id == "0":
#         return render_template(site.template+"/404.html"), 404
#     else:
#         if users.id == "None":
#             return redirect("/login")
#         else:
#             if users.id == "Master":
#                 value1 = request.form.get("value1")
#                 value2 =  request.form.get("value2")
#                 if value1.strip() == "" or value1 == None:
#                     return render_template(site.template+"/goto.html",message="공백또는 빈 컬쳐랜드 ID또는 PW는 허용하지 않습니다.", url="/setting/normal")
#                 if value2.strip() == "" or value2 == None:
#                     return render_template(site.template+"/goto.html",message="공백또는 빈 컬쳐랜드 ID또는 PW는 허용하지 않습니다.", url="/setting/normal")
#                 culture.edit(value1, value2)
#                 return render_template(site.template+"/goto.html",message="성공적으로 컬쳐랜드 정보를 변경했습니다.", url="/setting/normal")
#             else:
#                 return render_template(site.template+"/404.html"), 404

@app.route("/setting/normal/editCulture", methods=["POST"])
def setting_normal_editCulture():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value1 = request.form.get("value1")
                value2 =  request.form.get("value2")
                if value1.strip() == "" or value1 == None:
                    return render_template(site.template+"/goto.html",message="공백또는 빈 컬쳐랜드 ID또는 PW는 허용하지 않습니다.", url="/setting/normal")
                if value2.strip() == "" or value2 == None:
                    return render_template(site.template+"/goto.html",message="공백또는 빈 컬쳐랜드 ID또는 PW는 허용하지 않습니다.", url="/setting/normal")
                # culture.edit(value1, value2)
                database.update("sites", "culture", f"{value1}:{value2}",id=site.id)
                return render_template(site.template+"/goto.html",message="성공적으로 컬쳐랜드 정보를 변경했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404



@app.route("/setting/normal/editMusic", methods=["POST"])
def setting_normal_editMusic():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                musiclink: str = request.form.get("link").strip()
                if not musiclink.lower().endswith(".mp3"): return render_template(site.template+"/goto.html",message="파일 확장자는 MP3 만 가능합니다.", url="/setting/normal")
                if not musiclink.lower().startswith("https://cdn.discordapp.com/attachments/"): return render_template(site.template+"/goto.html",message="디스코드 CDN의 URL만 가능합니다.", url="/setting/normal")
                
                site.setMusic(musiclink)
                return render_template(site.template+"/goto.html",message="성공적으로 음악을 수정하였습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/normal/editRefer", methods=["POST"])
def setting_normal_editRefer():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                if value.strip() == "" or value == None:
                    return render_template(site.template+"/goto.html",message="추천인 적립금은 자연수만 허용합니다.", url="/setting/normal")
                try: value = int(value)
                except: return render_template(site.template+"/goto.html",message="추천인 적립금은 자연수만 허용합니다.", url="/setting/normal")
                if value < 0: return render_template(site.template+"/goto.html",message="추천인 적립금은 자연수만 허용합니다.", url="/setting/normal")
                database.update("sites", "refer_percent",value, id=site.id)
                
                return render_template(site.template+"/goto.html",message="성공적으로 추천인 적립금 변경했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/normal/editWebhook", methods=["POST"])
def setting_normal_editWebhook():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                site.setWebhook(value)
                return render_template(site.template+"/goto.html",message="성공적으로 웹훅을 변경했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/normal/editCultureDown", methods=["POST"])
def setting_normal_editCultureDown():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                if value.strip() == "" or value == None:
                    return render_template(site.template+"/goto.html",message="컬쳐랜드 수수료는 자연수만 허용합니다.", url="/setting/normal")
                try: value = int(value)
                except: return render_template(site.template+"/goto.html",message="컬쳐랜드 수수료는 자연수만 허용합니다.", url="/setting/normal")
                if value < 0: return render_template(site.template+"/goto.html",message="컬쳐랜드 수수료는 자연수만 허용합니다.", url="/setting/normal")
                site.setCulturedown(value)
                return render_template(site.template+"/goto.html",message="성공적으로 컬쳐랜드 수수료를 변경했습니다.", url="/setting/normal")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/category", methods=["GET", "POST"])
def setting_category():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                
                return render_template(site.template+"/setting_category.html",pl = len(database.select("product", site=site.id)), color=site.color(),plugin=database.select("sites",id=site.id)[0][18], username=users.id,category=product.category, useramount=users.amount, title=site.name,userrank=users.rank)
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/category/<int:id>/delete", methods=["POST"])
def setting_category_delete(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                database.delete("category", site=site.id, id=id)
                return render_template(site.template+"/goto.html",message="성공적으로 카테고리을 삭제했습니다.", url="/setting/category")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/category/create", methods=["POST"])
def setting_category_create():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                database.insert("category", site=site.id, name=random.genVerify())
                return render_template(site.template+"/goto.html",message="성공적으로 카테고리을 생성했습니다.", url="/setting/category")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/category/<int:id>/editName", methods=["POST"])
def setting_category_editName(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                print(value)
                database.update("category", "name", value, site=site.id, id=id)
                return render_template(site.template+"/goto.html",message="성공적으로 이름을 변경했습니다.", url="/setting/category")
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/products", methods=["GET", "POST"])
def setting_products():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                
                return render_template(site.template+"/setting_products.html", color=site.color(),pl = len(database.select("product", site=site.id)), category=product.category,plugin=database.select("sites",id=site.id)[0][18],username=users.id, useramount=users.amount, title=site.name,userrank=users.rank, product=product.productList)
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/delStock/<int:day>", methods=["POST"])
def setting_normal_delStock(id, day):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                product.delStock(id, value,day)
                return render_template(site.template+"/goto.html",message="성공적으로 재고를 삭제했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/setLow", methods=["POST"])
def setting_normal_setLow(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                database.update("product", "low", value, id=id)
                return render_template(site.template+"/goto.html",message="성공적으로 최소 구매  갯수를 설정했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/products/<int:id>/setCategory", methods=["POST"])
def setting_normal_setCategory(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                database.update("product", "category", value, id=id)
                return render_template(site.template+"/goto.html",message="성공적으로 카태고리를 설정했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/delAllStock/<int:day>", methods=["POST"])
def setting_normal_delAllStock(id, day):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                product.delAllStock(id, day)
                return render_template(site.template+"/goto.html",message="성공적으로 모든재고를 삭제했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/remove", methods=["POST"])
def setting_normal_remove(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                product.remove(id)
                return render_template(site.template+"/goto.html",message="성공적으로 상품을 삭제했습니다.", url="/setting/products")
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/addStock/<int:day>", methods=["POST"])
def setting_normal_addStock(id, day):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                database.addStock(site.id,id,value.split("\n"), day)
                return render_template(site.template+"/goto.html",message="성공적으로 상품 재고를 추가했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/editName", methods=["POST"])
def setting_normal_editName(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                product.updateName(id,value)
                return render_template(site.template+"/goto.html",message="성공적으로 상품 이름을 수정했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/editImage", methods=["POST"])
def setting_normal_editImage(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                
                product.updateImage(id,value)
                return render_template(site.template+"/goto.html",message="성공적으로 이미지을 수정했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404
@app.route("/setting/products/<int:id>/<int:day>/editLabel", methods=["POST"])
def setting_normal_editLabel(id,day ):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                
                product.updateLabel(value,id,day)
                return render_template(site.template+"/goto.html",message="성공적으로 라벨을 수정했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>/<rank>/<int:day>/editPrice", methods=["POST"])
def setting_normal_editPrice(id, rank, day):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                try: value = int(value)
                except: return render_template(site.template+"/goto.html",message="가격은 자연수만 허용합니다.", url="/setting/products/" + str(id))
                if value < 0: return render_template(site.template+"/goto.html",message="가격은 자연수만 허용합니다.", url="/setting/products/" + str(id))

                product.updatePrice(id, day, rank, value)
                return render_template(site.template+"/goto.html",message="성공적으로 상품 가격을 수정했습니다.", url="/setting/products/" + str(id))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/<int:id>", methods=["GET", "POST"])
def setting_product(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                category = database.select("category", site=site.id)
                return render_template(site.template+"/setting_products_edit.html",color=site.color(),plugin=database.select("sites",id=site.id)[0][18],category=category, username=users.id, useramount=users.amount, title=site.name,userrank=users.rank,p=product.getProduct(int(id)), s1=product.getAllStock(int(id), 1), s7=product.getAllStock(int(id), 7), s30=product.getAllStock(int(id), 30))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/products/createProduct", methods=["POST"])
def setting_products_createProduct():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                a = product.create()
                return render_template(site.template+"/goto.html",message=f"성공적으로 상품을 생성했습니다. (상품이름: {a})", url="/setting/products")
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/users", methods=["GET", "POST"])
def setting_users():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                all = users.usersList
                normal =  database.select("user", sites=site.id, rank="비구매자")
                pur = database.select("user", sites=site.id, rank="구매자")
                vip = database.select("user", sites=site.id, rank="VIP")
                reseller = database.select("user", sites=site.id, rank="리셀러")
                return render_template(site.template+"/setting_users.html",color=site.color(), category=product.category,plugin=database.select("sites",id=site.id)[0][18],username=users.id, title=site.name,useramount=users.amount, userrank=users.rank,users=all,type="총회원",all=len(all),normal=len(normal), pur=len(pur), vip=len(vip), reseller=len(reseller))
            else:
                return render_template(site.template+"/404.html"), 404

@app.route("/setting/users/<type>", methods=["GET", "POST"])
def setting_users_type(type):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                l = []
                all = users.usersList
                normal =  database.select("user", sites=site.id, rank="비구매자")
                pur = database.select("user", sites=site.id, rank="구매자")
                vip = database.select("user", sites=site.id, rank="VIP")
                reseller = database.select("user", sites=site.id, rank="리셀러")
                if type == "비구매자": l = normal
                elif type == "구매자": l = pur
                elif type == "VIP": l = vip
                elif type == "리셀러": l = reseller
                else:
                    type = "총회원"
                    l = all
                return render_template(site.template+"/setting_users.html",color=site.color(),plugin=database.select("sites",id=site.id)[0][18],username=users.id, title=site.name,useramount=users.amount, userrank=users.rank,users=l, type=type,all=len(all),normal=len(normal), pur=len(pur), vip=len(vip), reseller=len(reseller))

            else:
                return render_template(site.template+"/404.html"), 404


@app.route("/setting/user/<id>/editAmount", methods=["POST"])
def setting_users_editAmount(id):

    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                
                try: value = int(value)
                except: return render_template(site.template+"/goto.html",message="잔액은 자연수만 허용합니다.", url="/setting/products/" + str(id))
                if value < 0: return render_template(site.template+"/goto.html",message="잔액은 자연수만 허용합니다.", url="/setting/users")
                users.updateAmount(value, id)
                return render_template(site.template+"/goto.html",message="성공적으로 잔액을 수정했습니다.", url="/setting/users")
            else:
                return render_template(site.template+"/404.html"), 404


@app.route("/setting/user/<id>/editRank", methods=["POST"])
def setting_users_editRank(id):
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if users.id == "None":
            return redirect("/login")
        else:
            if users.id == "Master":
                value = request.form.get("value")
                ranks = ["VIP", "구매자", "리셀러", "비구매자"]
                if not value in ranks:
                    return render_template(site.template+"/goto.html",message="알 수 없는 랭크입니다.", url="/setting/users")
                users.updateRank(value, id)
                return render_template(site.template+"/goto.html",message="성공적으로 랭크를 수정했습니다.", url="/setting/users")
            else:
                return render_template(site.template+"/404.html"), 404

def createCloudflare(r):
    h = {
        "X-Auth-Email": "",
        "X-Auth-Key": "",
    }
    j = {
        "type":"A",
        "name":r,
        "content":"서버IP",
        "ttl":1,
        "proxied":True
    }
    res = requests.post(
        "https://api.cloudflare.com/client/v4/zones/CF_ZONE_ID/dns_records", 
        headers=h, 
        json=j
    )
    print(res.text)
    return res.text

@app.route("/purchase/<int:id>/<int:day>/<int:amount>")
def purchase(id, day,amount):
    
    p = product.getPrice(id,int(day))
    if p == None:
        return render_template(site.template+"/goto.html",message="잘못된 요청입니다.", url="/list")
    

    price = int(p) * amount
    if price == 0:
        return render_template(site.template+"/goto.html",message="비활성화 된 상품입니다.", url="/list")
    if price > users.amount:
        return render_template(site.template+"/goto.html",message="잔액이 부족합니다. 충전신청후 이용해주세요.", url="/list")
    stocks = product.getAllStock(id,day)

    u = database.select("user", name=users.id, sites=site.id)
    uid = str(u[0][7])
    g = database.select("sites", id=site.id)[0]

    gid = str(g[13])
    rid = str(g[14])
    

    low = int(database.select("product", id=id)[0][5])
    if low > amount:
        return render_template(site.template+"/goto.html",message=f"최소 구매 가능갯수를 맞춰 주세요. ({low})", url="/list")
    if len(stocks) < amount:
        return render_template(site.template+"/goto.html",message="재고가 없습니다. 나중에 다시 구매시도를 부탁드립니다.", url="/list")

    if users.rank == "비구매자":
        users.updateRank("구매자")
    aaa = product.getStock(id,day,amount)
    users.updateAmount(users.amount - price)
    buyamount = price + int(database.select("user", name=users.id,sites=site.id)[0][11])
    database.update("user", "buyamount", buyamount, name=users.id,sites=site.id)

    try:
        refer_pencent = database.select("sites", id=site.id)[0][19]
        refer_by = database.select("user", name=users.id)[0][9]
        _refer_ = database.select("user", sites=site.id, name=refer_by)[0]
        refer_by_amount = _refer_[4]
        refer_give = (price // 100) * (refer_pencent)
        # 1 * 100 - 12
        print(refer_by_amount, refer_give, int(refer_by_amount) + refer_give)
        database.update("user", 'money',int(refer_by_amount) + refer_give,sites=site.id, name=refer_by)
    except:
        pass
    
    headers = {
        "Authorization": "Bot 봇토큰"
    }
    a = requests.put(f"https://discord.com/api/guilds/{gid}/members/{uid}/roles/{rid}", headers=headers)

    return render_template(site.template+"/pur.html",message='코드로그를 확인해 주세요.', url="/list")
@app.route("/culture", methods=['POST'])
def _culture():
    if site.id == "0":
        return render_template(site.template+"/404.html"), 404
    else:
        if site.culture == None or site.culture == "" or site.culture == "null":
            return "문화상품권 자동충전이 비활성화 되어 있습니다."
        c = site.culture.split(":")
        amount, message = Auto.CulturelandAutoCharge(c[0], c[1], request.form.get("code"))
        if amount != 0:
            amount = int(amount)
            amount = (amount // 100) * (100 - site.culturedown)
            users.updateAmount(users.amount + amount)
            return {"result": True, "message": message, "amount": amount}
        else:
            return {"result": False, "message": message, "amount": amount}
    
@app.errorhandler(404)
def notfound(e):
    return render_template(site.template+"/404.html"), 404

if __name__ == "__main__":
    app.run("0.0.0.0", 80)
