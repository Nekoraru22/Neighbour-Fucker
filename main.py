from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from colorama import Fore, init
from datetime import datetime
from IA.mainAI import AI
from os import walk
import time, json, emoji, os, random, re, string, urllib.request
init()

####### COLORS #######
RED = Fore.LIGHTRED_EX
GREEN = Fore.LIGHTGREEN_EX
YELLOW = Fore.LIGHTYELLOW_EX
BLUE = Fore.LIGHTBLUE_EX
MAGENTA = Fore.LIGHTMAGENTA_EX
CYAN = Fore.LIGHTCYAN_EX
WHITE = Fore.LIGHTWHITE_EX
RESET = Fore.RESET

####### GLOBALS #######
__API_KEY__ = "key"
__FIRST_MESSAGE__ = "Hi, F 21"
__LAST_MESSAGE__ = "I have to close, send me a msg or call me on Whats App, i let you my number <3 +34 xxx xx xx xx"

####### DIRECTORIES #######
if not os.path.exists("conversations"): os.makedirs("conversations")
if not os.path.exists("strangerPics"): os.makedirs("strangerPics")
if not os.path.exists("images"): os.makedirs("images")

def getDriver():
    s = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(service=s, options=options)

    return driver

def filtro(string: str) -> str:
    to_filter = {
        "masturbate": "mast urbate",
        "whatsapp": "whats app",
        "snapchat": "snap chat",
        "money": "mone y",
        "horny": "horni",
        "assistant": "",
        "human: ": "",
        "fuck": "fuk",
        "dick": "dik",
        "cock": "cok",
        "sex": "se x",
        "ai: ": "",
        " ai": "",
        "!": ""
    }

    for key in to_filter.keys():
        if key in string: string = string.replace(key, to_filter[key])
    
    return string

def id_generator(size: int =6, chars: str =string.ascii_uppercase + string.digits) -> str:
    return ''.join(random.choice(chars) for _ in range(size))

def normalice(string: str) -> str:
    try:
        x = re.match(r'.+(:\/\/)strangermeetup.com/content/uploads/messages/', string)
        y = string.replace(x.group(0), "")
    except: pass

    try: return f"{y}.png"
    except: return f"{id_generator()}.png"

def imgDownload(url: str) -> None:
    try:
        name = normalice(url)
        urllib.request.urlretrieve(url, f"strangerPics/{name}")
    except: pass

def typing(string: str) -> str:
    print(f"[·] {string} - Time: {int(len(string)/10)}")
    time.sleep(int(len(string)/10))
    return string

def sendImg(driver: any, order: int) -> None:
    files = []
    for (dirpath, dirnames, filenames) in walk("images"):
        files.extend(filenames)
        break

    if order > len(files): order = len(filenames)

    time.sleep(1.5)
    driver.find_elements(By.CLASS_NAME, "action-toggler")[0].click()
    time.sleep(1)

    driver.find_element(By.ID, "photo").send_keys(os.getcwd() + f"/images/{order}.png")

    time.sleep(1)
    driver.find_elements(By.CLASS_NAME, "submit-btn")[0].click()

    print(f"{MAGENTA}[{WHITE}{order}{MAGENTA}] Picture sent{RESET}")

def sendMsg(driver: any, msg: str) -> None:
    final = filtro(msg.lower())
    if final[-1] == ".": final = final[:-1]

    try:
        driver.find_element(By.ID, "text").send_keys(final)
        time.sleep(1)
        driver.find_elements(By.CLASS_NAME, "send-button")[0].click()
    except: pass

def main():
    IA = AI(__API_KEY__)

    last_author = None
    friend = None
    messages = {}
    downloaded = []
    limit = 30
    counter = 0
    me = None
    pic_order = 1

    print(f"{GREEN}[{WHITE}·{GREEN}] Bot started{RESET}")

    driver = getDriver()
    driver.get("https://strangermeetup.com/chat")
    driver.add_cookie({"name":"express.sid", "value":"s%3AgCuopqO_NmneCu90BiWVAuEEno0WEB0M.wH976zYdzx81Eird6mnTFkIGahkIeKy7jN7j%2FZLLeoo"})
    time.sleep(1)
    driver.get("https://strangermeetup.com/chat")
    time.sleep(0.5)
    try: driver.find_elements(By.CLASS_NAME, "fc-cta-consent")[0].click()
    except: pass

    time.sleep(2)
    sendMsg(driver, __FIRST_MESSAGE__)

    while True:
        pict = ""

        try:
            chat = driver.find_element(By.ID, "chat")
            msgs = chat.find_elements(By.CLASS_NAME, "message-text")
            author = chat.find_elements(By.XPATH, "//span[@class='user-alias']")[:-1]
            imgs = chat.find_elements(By.CLASS_NAME, "image-upload")
            
            if len(downloaded) != len(imgs):
                for x in imgs:
                    if x.get_attribute("src") in downloaded: continue
                    print(f'{GREEN}[{WHITE}·{GREEN}] Downloading image: {RESET}{x.get_attribute("src")}')
                    imgDownload(x.get_attribute("src"))
                    downloaded.append(x.get_attribute("src"))
                    pict = x

            if pict:
                container[index] = {"author": "image", "msg": pict.get_attribute("src")}
                index += 1

            index = 0
            container = {}
            for x in range(len(msgs)):
                if str(msgs[x].text) == __FIRST_MESSAGE__.lower(): me = author[x].get_attribute("innerHTML")
                container[index] = {"author": author[x].get_attribute("innerHTML"), "msg": msgs[x].text}
                index += 1

            if len(container.values()) > 0:
                last_author = author[-1].get_attribute("innerHTML")

            if last_author and last_author != me: friend = last_author # "Valeria2001"
            else: last_author = None

            if len(messages.values()) != len(container.values()) and last_author:
                messages = container

                def recursiveAuthor(i):
                    if i - 1 < 0: return messages[i]["msg"]
                    if messages[i - 1]["author"] == last_author: return recursiveAuthor(i - 1) + " " + messages[i]["msg"]
                    return messages[i]["msg"]

                questions = recursiveAuthor(index - 1).replace(__FIRST_MESSAGE__, "")
                if questions.lower() == "ok": continue
                
                try: resp = IA.question(emoji.demojize(questions, delimiters=("", " ")))
                except:
                    print(f"{RED}[{WHITE}·{RED}] API not working{RESET}")
                    break

                sendMsg(driver, typing(resp))
                
                for x in [" pic", "photo", "nudes", "selfie"]:
                    if x in resp:
                        sendImg(driver, pic_order)
                        pic_order += 1

                        time.sleep(5)
                        downloaded.append(chat.find_elements(By.CLASS_NAME, "image-upload")[-1].get_attribute("src"))

            if len(driver.find_elements(By.CLASS_NAME, "room-user-list")[0].find_elements(By.TAG_NAME, "span")) < 8:
                if len(messages.values()) > 0 and friend:
                    filename = str(datetime.now().strftime("%d-%m-%Y_%H;%M;%S"))

                    with open(f"conversations/({friend})_{filename}.json", "w+") as file:
                        file.write(json.dumps(messages, indent=4, sort_keys=True))

                    print(f"{YELLOW}[{WHITE}·{YELLOW}] New conversation started{RESET}")

                IA.clear()
                driver.get("https://strangermeetup.com/chat")
                time.sleep(2)
                sendMsg(driver, __FIRST_MESSAGE__)

                downloaded = []
                pic_order = 1
                counter = 0

            time.sleep(5)
            if counter >= limit:
                sendMsg(driver, __LAST_MESSAGE__)
                time.sleep(5)
                sendMsg(driver, "See you <3")
                time.sleep(3)

                if len(messages.values()) > 0 and friend:
                    filename = str(datetime.now().strftime("%d-%m-%Y_%H;%M;%S"))

                    with open(f"conversations/({friend})_{filename}.json", "w+") as file:
                        file.write(json.dumps(messages, indent=4, sort_keys=True))

                    print(f"{YELLOW}[{WHITE}·{YELLOW}] New conversation started{RESET}")

                IA.clear()
                driver.get("https://strangermeetup.com/chat")
                time.sleep(2)
                sendMsg(driver, __FIRST_MESSAGE__)

                downloaded = []
                pic_order = 1
                counter = 0

                driver.get("https://strangermeetup.com/chat")
                time.sleep(1)
                driver.switch_to.alert.accept()
                time.sleep(2)

                downloaded = []
                pic_order = 1
                counter = 0

            counter += 1
        except: continue

if __name__ == "__main__":
    main()