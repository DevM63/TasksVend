from selenium import webdriver
import os, time, threading
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import JavascriptException
ms3 = 0


def showTime(name, ms):
    global ms3
    ms2 = time.time_ns() // 1000000 
    result = ms2 - ms
    result2 = ms2 - ms3
    ms3 = ms2
    print(f"[!] TIME: {result}ms | {result2}ms | {name}")
using = []






def CulturelandAutoCharge(token, code):
    global ms3
    
    ms = time.time_ns() // 1000000 
    ms3 = ms
    try:
        cc = 0
        csp = code.split("-")
        for i in csp: 
            int(i)
            if cc == 3 and (len(i) != 6 and len(i) != 4):
                return (0, "문화상품권 코드가형식에 맞지 않습니다.")
            if cc != 3 and len(i) != 4:
                return (0, "문화상품권 코드가형식에 맞지 않습니다.")
            cc +=  1
                
        if len(csp) != 4: 
            return (0, "문화상품권 코드가형식에 맞지 않습니다.")
    except:
        return (0, "문화상품권 코드가형식에 맞지 않습니다.")
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"#"none"
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path='./chromedriver.exe', options=chrome_options)

    showTime("Loading Site",ms)  
    driver.get('https://m.cultureland.co.kr/ext/mTranskey/transkey_mobile/images/0.png')
    showTime("Input Login Info",ms)
    while True:
        try:
            driver.add_cookie({'name':'KeepLoginConfig','value' :token})
            break
        except:
            pass
        
    showTime("Loading loginMain [POST]",ms)
    driver.get('https://m.cultureland.co.kr/mmb/loginMain.do')
    
    # if driver.current_url == "https://m.cultureland.co.kr/mmb/loginMain.do":
        # using.remove(port)
        # return (0, "아이디 비번이 정확하지 않습니다.")  

    

    
    showTime("Loading cshGiftCard",ms)
    driver.get("https://m.cultureland.co.kr/csh/cshGiftCard.do")
    def clickKey(name): driver.execute_script(f""" document.querySelector('[alt="{name}"]').parentElement.parentElement.onmousedown() """)
    time.sleep(0.33)


    showTime("Input Pin Code",ms)
    try:

    
        driver.execute_script(f"""document.querySelector("input[id='txtScr11']").value="{csp[0]}";""")
        driver.execute_script(f"""document.querySelector("input[id='txtScr12']").value="{csp[1]}";""")
        driver.execute_script(f"""document.querySelector("input[id='txtScr13']").value="{csp[2]}";""")
        try: driver.find_element_by_id("txtScr14").send_keys('\n') 
        except: pass 

        l = list(csp[3])

        for ii in l: clickKey(ii)
        
        try: clickKey("입력완료")
        except: pass 
        

    except Exception as e:
        driver.close()
        return (0, "올바른 형식으로 핀번호를 입력해 주세요.")
    showTime("Send Pin Code",ms)
    driver.execute_script("document.getElementById('btnCshFrom').click()")
    
    showTime("Get Result",ms)
    time.sleep(0.1)
    if driver.current_url.startswith("https://m.cultureland.co.kr/mmb/loginMain.do"):
        driver.close()
        return (0, "아이디 비번이 정확하지 않습니다.")  
    while True:
        try:
            driver.find_element_by_tag_name("dd")
            break
        except:
            pass
    amount = int(driver.find_element_by_tag_name("dd").text.replace("원", "").replace(",",""))
    message =  driver.find_element_by_tag_name("b").text
    showTime(code,ms)
    driver.close()
    return (amount, message)
    



def CulturelandGetToken(id,pw):
    Options = webdriver.chrome.options.Options()  
    chrome_prefs = {}
    Options.experimental_options["prefs"] = chrome_prefs
    Options.add_argument("start-maximized") 
    Options.add_argument("disable-infobars")
    #Options.binary_location = "y:/chrome.exe"
    chrome_prefs["profile.default_content_settings"] = {"images": 2}
    chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
    driver2 = webdriver.Chrome(executable_path='./chromedriver.exe', chrome_options=Options)
    

    driver2.get('https://m.cultureland.co.kr/mmb/loginMain.do')

    spdict = {
        "": "어금기호",
        "~": "물결표시",
        "!": "느낌표",
        "@": "골뱅이",
        "#": "샾",
        "$": "달러기호",
        "%": "퍼센트",
        "^": "꺽쇠",
        "&": "엠퍼샌드",
        "*": "별표",
        "(": "왼쪽괄호",
        ")": "오른쪽괄호",
        "-": "빼기",
        "_": "밑줄",
        "=": "등호",
        "+": "더하기",
        "[": "왼쪽대괄호",
        "{": "왼쪽중괄호",
        "]": "오른쪽대괄호",
        "}": "오른쪽중괄호",
        "\\": "역슬래시",
        "|": "수직막대",
        ";": "세미콜론",
        ":": "콜론",
        "/": "슬래시",
        "?": "물음표",
        ",": "쉼표",
        "<": "왼쪽꺽쇠괄호",
        ".": "마침표",
        ">": "오른쪽꺽쇠괄호",
        "'": "작은따옴표",
        '"': "따옴표",


    }


    
    driver2.execute_script(f"""document.querySelector("input[id='txtUserId']").value="{id}";""")
    driver2.find_element_by_id("passwd").click()
    time.sleep(0.2)
    def isChar():
        element_count = len(driver2.find_elements_by_css_selector(f'[alt="따옴표"]'))
        if element_count == 0:
            return True
        else:
            return False
        
    def clickKey(name): driver2.execute_script(f""" document.querySelector('[alt="{name}"]').parentElement.parentElement.onmousedown() """)
    def shift(): driver2.execute_script(f"""mtk.cap(event, this);""")
    def change(): driver2.execute_script(f"""mtk.sp(event, this);""")
        
    change()
    for i in list(pw):

        if i.lower() in list("abcdefghijklmnopqrstuvwxyz1234567890"):
            if not isChar():
                change()
            if i in list("ABCDEFGHIJKLMNOPQRSTUVWXYZ"):
                shift()
                clickKey("대문자"+i)
                shift()
            else: 
                clickKey(i)
        else:
            if isChar():
                change()
            clickKey(spdict[i])
    try:
        clickKey("입력완료")
    except:
        pass
    driver2.execute_script("document.getElementById('chkKeepLogin').click()")
    

    driver2.find_element_by_id("btnLogin").click()
    if driver2.current_url == "https://m.cultureland.co.kr/mmb/loginMain.do":
        driver2.close()
        return (False, "아이디 비번이 정확하지 않습니다.", "")
    token = str(driver2.get_cookie("KeepLoginConfig")['value'])
    driver2.close()
    return (True, "성공적으로 로그인이 완료되었습니다.", token)
