import requests
import json

url = 'https://v2.jokeapi.dev/joke/Any'

def get_joke(contains=None, *, user):
    params = {'safe-mode': None, 'type': 'single'}
    if contains is not None:
        params['contains'] = contains
    blacklist = get_user_blacklist(user)
    for _ in range(5):
        response = requests.get(url, params=params)
        data = json.loads(response.text)
        if data['error']:
            break
        joke_lower = data['joke'].lower()
        flag = False
        for word in blacklist:
            if word in joke_lower:
                flag = True
                break
        if flag:
            continue
        return data['joke']
    return 'No jokes(('


def get_user_blacklist(user):
    user = str(user)
    with open('blacklist.json') as file:
        data = json.loads(file.read()) 
        if user in data: 
            return data[user]
        else:
            return []
        
def update_user_blaklist(user, new_blacklist): 
    user = str(user)
    with open('blacklist.json') as file:
        data = json.loads(file.read()) 
    
    if not user in data:
        data[user] = []

    with open('blacklist.json', 'w+') as file:
        data[user] += new_blacklist
        print(data)
        file.write(json.dumps(data))

def clear_user_blacklist(user):
    user = str(user)
    with open('blacklist.json') as file:
        data = json.loads(file.read()) 

    with open('blacklist.json', 'w+') as file:
        data[user] = []
        print(data)
        file.write(json.dumps(data))
