import requests
import json
import time
from tqdm import tqdm

# data user
RESP_URL = 'https://api.vk.com/method/'
APP_ID = 171691064
ACCESS_TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'
USER_NAME = 'eshmargunov'
# list parametr
params_friends = {
    'v': 5.52,
    'access_token': ACCESS_TOKEN
}

params_groups = {
    'v': 5.52,
    'access_token': ACCESS_TOKEN,
    'user_id': APP_ID
}

params_info_groups = {
    'v': 5.52,
    'access_token': ACCESS_TOKEN,
    'group_ids': None
}

params_members_groups = {
    'v': 5.52,
    'access_token': ACCESS_TOKEN,
    'group_id': None
}
# list method
method_friends = 'friends.get'
method_groups = 'groups.get'
method_info_groups = 'groups.getById'
method_members_groups = 'groups.getMembers'

print(f'Получения списка id групп и друзей пользователя {USER_NAME}')
list_id_groups = requests.get(f'https://api.vk.com/method/{method_groups}', params=params_groups).json()['response']['items']
list_id_friends = requests.get(f'https://api.vk.com/method/{method_friends}', params=params_friends).json()['response']['items']

set_id_group = set(list_id_groups)  # change list in set for difference sets

print(f'Отправка запросов к API VK для получения списка групп друзей пользователя {USER_NAME}')
for id_friend in tqdm(list_id_friends, ncols=100):
    params_groups['user_id'] = id_friend
    try:
        # request for make set user's friends groups
        set_id_friend_group = set(
            requests.get(f'https://api.vk.com/method/{method_groups}', params=params_groups).json()['response']['items'])
    except KeyError:
        continue
    personal_group = set_id_group.difference(set_id_friend_group)  # difference sets for make list groups only user
    set_id_group = personal_group
    time.sleep(0.2)
personal_group = list(personal_group)

params_info_groups['group_ids'] = str(personal_group).strip('[]')

info_groups = requests.get(f'https://api.vk.com/method/{method_info_groups}', params=params_info_groups).json()["response"]

count_members_group = []
for id_group in personal_group:
    params_members_groups['group_id'] = id_group
    count_members_group.append(
        requests.get(f'https://api.vk.com/method/{method_members_groups}', params=params_members_groups).json()['response']['count'])
    time.sleep(0.34)
print('Преобразование полученный данных')
for_write = []
for group in tqdm(range(len(personal_group)), ncols=90):
    for_write.append({'name': info_groups[group]['name'], 'gid': info_groups[group]['id'], 'member_count': count_members_group[group]})

with open('groups.json', 'w', encoding='utf-8') as groups:
    json.dump(for_write, groups, ensure_ascii=False, indent=2)
