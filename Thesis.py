import requests
import json
import time
from tqdm import tqdm

def data(): # return RESP_URL, APP_ID, ACCESS_TOKEN, USER_NAME
    RESP_URL = 'https://api.vk.com/method/'
    APP_ID = 171691064
    ACCESS_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
    USER_NAME = 'eshmargunov'
    return RESP_URL, APP_ID, ACCESS_TOKEN, USER_NAME
# return RESP_URL, APP_ID, ACCESS_TOKEN, USER_NAME

def params(data=data()): # return params_friends, params_groups, params_groups_friends, params_info_groups,
    # params_members_groups
    params_friends = {
        'v': 5.52,
        'access_token': data[2]
    }

    params_groups = {
        'v': 5.52,
        'access_token': data[2],
        'user_id': data[1]
    }

    params_info_groups = {
        'v': 5.52,
        'access_token': data[2],
        'group_ids': None
    }

    params_members_groups = {
        'v': 5.52,
        'access_token': data[2],
        'group_id': None
    }

    return params_friends, params_groups, params_info_groups, params_members_groups
# return params_friends, params_groups, params_info_groups, params_members_groups

def methods():
    method_friends = 'friends.get'
    method_groups = 'groups.get'
    method_info_groups = 'groups.getById'
    method_members_groups = 'groups.getMembers'
    return method_friends, method_groups, method_info_groups, method_members_groups
#return method_friends, method_groups, method_info_groups, method_members_groups

def display(data=data(), method=methods(), params=params()):
    count_friends = requests.get(f'{data[0]}{method[0]}', params[0]).json()['response']['count']
    count_groups = requests.get(f'{data[0]}{method[1]}', params[1]).json()['response']['count']
    print(f'''Данный файл выполняет серию запросов к API VK от имени пользователя {data[3]}, id которого {data[1]}.
На данный момент количество друзей пользователя составляет: {count_friends}
                 количество групп пользователя составляет: {count_groups}''')

def body(data = data(), method = methods(), params = params()):
    print(f'Получения списка id групп и друзей пользователя {data[3]}')
    list_id_groups = requests.get(f'https://api.vk.com/method/{method[1]}', params=params[1]).json()['response']['items']
    list_id_friends = requests.get(f'https://api.vk.com/method/{method[0]}', params=params[0]).json()['response']['items']

    set_id_group = set(list_id_groups)  # change list in set for difference sets

    print(f'Отправка запросов к API VK для получения списка групп друзей пользователя {data[3]}')
    for id_friend in tqdm(list_id_friends, ncols=100):
        params[1]['user_id'] = id_friend
        friend_group = requests.get(f'https://api.vk.com/method/{method[1]}', params=params[1]).json()
        if 'response' in friend_group.keys():
            set_id_friend_group = friend_group['response']['items']

        personal_group = set_id_group.difference(set_id_friend_group)  # difference sets for make list groups only user
        set_id_group = personal_group
        time.sleep(0.34)
    personal_group = list(personal_group)

    params[2]['group_ids'] = str(personal_group).strip('[]') # transform id group in string for params

    time.sleep(0.34)
    info_groups = requests.get(f'https://api.vk.com/method/{method[2]}', params=params[2]).json()["response"]


    count_members_group = []
    for id_group in personal_group:
        params[3]['group_id'] = id_group
        count_members_group.append(
            requests.get(f'https://api.vk.com/method/{method[3]}', params=params[3]).json()['response']['count'])
        time.sleep(0.34)
    print('Преобразование полученный данных')
    for_write = []
    for group in tqdm(range(len(personal_group)), ncols=90):
        for_write.append({'name': info_groups[group]['name'], 'gid': info_groups[group]['id'], 'member_count': count_members_group[group]})

    with open('groups.json', 'w', encoding='utf-8') as groups:
        json.dump(for_write, groups, ensure_ascii=False, indent=2)

while True:
    display()
    body()
    print('Выполнение закончено! В каталоге программы создан/перезаписан файл groups.json')
    print('Хотите повторить операцию? (да или нет)')
    if not input().lower().startswith('д'):
        break