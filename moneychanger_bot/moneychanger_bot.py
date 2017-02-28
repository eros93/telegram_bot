import json
import requests
import pycountry

TOKEN = "379375536:AAE_YgQiOmZ4EfWdUAYsIf2IYKHP_8TOJR0"
URL = "https://api.telegram.org/bot{}/".format(TOKEN)

def get_url(url,retries=0):
    if retries > 10: return NameError
    try:
        response = requests.get(url, timeout=10)
        content = response.content.decode("utf8")
        return content
    except:
        retries+=1
        get_url(url,retries)


def get_me():
    url = URL + "getme"
    js = get_json_from_url(url)
    #prettyprint_json(js)
    return js

def get_json_from_url(url):
    content = get_url(url)
    js = json.loads(content)
    return js

def prettyprint_json(js):
    print json.dumps(js,sort_keys=True, indent=4, separators=(',',': '))


def get_updates(offset=None):
    url = URL + "getUpdates?timeout=100"
    if offset:
        url += "&offset={}".format(offset)
    js = get_json_from_url(url)
#    print prettyprint_json(js)
    return js

def get_last_update_id(updates):
    update_ids = []
    for update in updates["result"]:
        update_ids.append(int(update["update_id"]))
    #print max(update_ids)
    return max(update_ids)

def get_last_chat_id_and_text(updates):
    num_updates = len(updates["result"])
    last_update = num_updates - 1 # perche abbiamo la numerazione da 0
    text = updates["result"][last_update]["message"]["text"]
    chat_id = updates["result"][last_update]["message"]["chat"]["id"]
    #print (text,chat_id)
    return (text, chat_id)

def send_message(text, chat_id, reply_markup=None):
    url = URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
    if reply_markup:
        url += "&reply_markup={}".format(reply_markup)
    return get_url(url)

def country_to_abbrev(country):
    germany = pycountry.countries.get(name=country)
    tmp = germany.alpha_3
    print tmp
    return tmp


def get_moneyupdate(state):
    url = "https://api.fixer.io/latest"
    money = get_json_from_url(url)
    #based on euro
    value = money ["rates"][state]
    prettyprint_json(money)
    print value

def build_keyboard(items):
    keyboard = [[item] for item in items]
    reply_markup = {"keyboard":keyboard, "one_time_keyboard":True}
    return json.dumps(reply_markup)



def main():
    js = get_updates()
    currency = country_to_abbrev('Poland')
    print currency
    currency = "PLN"
    get_moneyupdate(currency)
    (temp,chatID)=get_last_chat_id_and_text(js)
    text = "ciao i'm a bot"
    item = []
    item = ['dollar_USA', 'zloty_Poland)', 'Yen_Giapan']
    print item
    keyboard = build_keyboard(item)
    content = send_message(text,chatID,keyboard)
    js = json.loads(content)
    prettyprint_json(js)

#def main():
#    last_update_id =None
#    while True:
#        updates = get_updates(last_update_id)
#        if len(updates["result"]) > 0:
#            last_update_id = get_last_update_id(updates) + 1
#            handle_updates(updates)
#        time.sleep(0.5)

if __name__=='__main__':
    main()