### Python interface to some bbox3v user configuration tools
### Sebastien Blaise, 2016

### A file named "userPassword" should be created in the same directory, containing the User bbox3 password
### A file named "hostName" should be created in the same directory, containing the bbox3 password host name without http://


import hashlib
import re
import mechanize

def login(user, pwd):
    realm = "Technicolor Gateway";
    qop = "auth"
    uri = "/login.lp"
    initPage = browser.open(host+"/login.lp")
    for line in initPage.read().split('\n'):
        if (line[0:9] == "var nonce"):
            nonce = line[13:-3]
    md5 = hashlib.md5()
    md5.update(user + ":" + realm + ":" + pwd)
    HA1 = md5.hexdigest()
    md5 = hashlib.md5()
    md5.update("GET" + ":" + uri)
    HA2 = md5.hexdigest()
    md5 = hashlib.md5()
    md5.update(HA1 + ":" + nonce + ":" + "00000001" + ":" + "xyz" + ":" + qop + ":" + HA2)
    hidepw = md5.hexdigest()
    browser.select_form(name = "authform")
    browser.form.find_control("hidepw").readonly = False
    browser.form['hidepw'] = hidepw
    browser.submit()

def antiCSRF(browser, cj):
    browser.form.new_control('text','rn',{'value':''})
    browser.form.fixup()
    browser.form['rn'] = cj[0].value

def reboot(browser, cj):
    browser.open(host+"/bbox-maintenance.lp")
    browser.select_form(nr = 0)
    antiCSRF(browser, cj)
    browser.form.find_control("main_reboot").readonly = False
    browser.form['main_reboot'] = "1"
    browser.submit()

def switchVoice1(browser, cj, state):
    browser.open(host+"/voice-line-1.lp")
    browser.select_form(name = "voice1")
    antiCSRF(browser, cj)
    browser.form.find_control("voice1_enable").readonly = False
    if (state):
        browser.form['voice1_enable'] = "1"
    else:
        browser.form['voice1_enable'] = "0"
    browser.submit()

def setVoice1Port(browser, cj, port):
    browser.open(host+"/voice-line-1.lp")
    browser.select_form(name = "voice1")
    antiCSRF(browser, cj)
    oldPort = browser.form['RSPort1']
    browser.form['RSPort1'] = port
    browser.submit()
    return oldPort

def stripHTML(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)

    
def getIP(browser, cj, index):
    page = browser.open(host+"/network-global.lp")
    found = 0
    remaining = 0
    for line in page.read().split('\n'):
        remaining -= 1
        if (remaining == 0):
            break
        if "IPv4" in line:
            found += 1
            if (found == index+1):
                remaining = 2
    return stripHTML(line).strip()

def getInternetIP(browser, cj):
    return getIP(browser, cj, 0)

def getVideoIP(browser, cj):
    return getIP(browser, cj, 1)

def getVoiceIP(browser, cj):
    return getIP(browser, cj, 2)


user = "User"
### Insert your User password in the userPassword file
with open('userPassword', 'r') as f:
    pwd = f.readline()
### Insert your bbox3 hostname (without http://) in the userPassword file
with open('hostName', 'r') as f:
    host = "http://"+f.readline()

    
browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

cj = mechanize.LWPCookieJar()
browser.set_cookiejar(cj)

login(user, pwd)

### Available commands
#switchVoice1(browser, cj, False)
#switchVoice1(browser, cj, True)
#reboot(browser, cj)
print("Internet IP: %s"%getInternetIP(browser, cj))
print("Video IP: %s"%getVideoIP(browser, cj))
print("Voice IP: %s"%getVoiceIP(browser, cj))
oldPort = setVoice1Port(browser, cj, "5070")
print("Switching sip port from %s to 5070"%oldPort)
print("Switching back sip port from %s to %s"%(setVoice1Port(browser, cj, oldPort), oldPort))

