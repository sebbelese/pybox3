### Python interface to some bbox3v user configuration tools
### Sebastien Blaise, 2016

import hashlib
import re
import mechanize

def login(user, pwd):
    realm = "Technicolor Gateway";
    qop = "auth"
    uri = "/login.lp"
    initPage = browser.open("http://192.168.1.1/login.lp")
    for line in initPage.read().split('\n'):
        if (line[0:9] == "var nonce"):
            nonce = line[13:-3]
    print nonce
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
    browser.open("http://192.168.1.1/bbox-maintenance.lp")
    browser.select_form(nr = 0)
    antiCSRF(browser, cj)
    browser.form.find_control("main_reboot").readonly = False
    browser.form['main_reboot'] = "1"
    browser.submit()

def switchVoice(browser, cj, state):
    browser.open("http://192.168.1.1/voice-line-1.lp")
    browser.select_form(name = "voice1")
    antiCSRF(browser, cj)
    browser.form.find_control("voice1_enable").readonly = False
    if (state):
        browser.form['voice1_enable'] = "1"
    else:
        browser.form['voice1_enable'] = "0"
    browser.submit()

user = "User"
### Insert your User password here
pwd = "XXXXXXXX"

browser = mechanize.Browser()
browser.set_handle_robots(False)
browser.addheaders = [("User-agent","Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.2.13) Gecko/20101206 Ubuntu/10.10 (maverick) Firefox/3.6.13")]

cj = mechanize.LWPCookieJar()
browser.set_cookiejar(cj)

login(user, pwd)

### Available commands
switchVoice(browser, cj, False)
#switchVoice(browser, cj, True)
#reboot(browser, cj)
