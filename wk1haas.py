from cgitb import strong
from itertools import tee
from posixpath import split
from matplotlib.pyplot import text
import requests
import json
import urllib.parse

API_ENDPOINT = "https://haas.quoccabank.com"

#####################
# First post request
#####################
headers = {
    "Host": "haas.quoccabank.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "11",
    "Origin": "https://haas.quoccabank.com",
    "Referer": "https://haas.quoccabank.com/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Te": "trailers",
    "Connection": "close",
    "Action": "haas.quoccabank.com",
}

r = requests.post(url=API_ENDPOINT, data={"requestBox": ""}, headers=headers)

print(r.text + '\n')

####################
# Calculations
####################


def getCalculation(text):
    split_text = text.split('\n')
    math_question = ""
    for line in split_text:
        if "What is" in line:
            math_question = line
    numbers_to_add = math_question.split(' ')[-1].replace('?', "").split('+')
    sum = 0
    for num in numbers_to_add:
        sum += int(num)
    return sum


def getCookieSession(text):
    split_text = text.split('\n')
    cookie_line = ""
    for line in split_text:
        if "Set-Cookie" in line:
            cookie_line = line
    cookie_trimmed = " ".join(cookie_line.split(
        " ")[0:2]).replace(";", "").replace('Set-Cookie: ', "")
    return cookie_trimmed


calculation_header = {
    "Host": "haas.quoccabank.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": str(7+len(str(getCalculation(r.text)))),
    "Origin": "https://haas.quoccabank.com",
    "Referer": "https://haas.quoccabank.com/",
    "Upgrade-Insecure-Requests": "1",
    "Sec-Fetch-Dest": "document",
    "Sec-Fetch-Mode": "navigate",
    "Sec-Fetch-Site": "same-origin",
    "Te": "trailers",
    "Action": "haas.quoccabank.com",
}

str_only = """POST / HTTP/1.1
Host: haas.quoccabank.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:101.0) Gecko/20100101 Firefox/101.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded
Content-Length: {2}
Origin: https://haas.quoccabank.com/
Referer: https://haas.quoccabank.com/
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Connection: keep-alive
Te: trailers
Cookie: {0}

answer={1}"""

for count in range(1, 22):
    print('------ {} ------'.format(count))
    formatted_request_box_input = str_only.format(getCookieSession(
        r.text), str(getCalculation(r.text)), str(7+len(str(getCalculation(r.text)))))
    r = requests.post(url=API_ENDPOINT, data={
        "requestBox": formatted_request_box_input}, headers=calculation_header)
    print(r.text)
    print('\n')
