from platform import platform
import requests
import re
from origin_connector import origin_api
from utils.sync_values import get_unknowns_keys
from time import sleep


i = 0
while True:
    i += 1
    sleep(2)
    try:
        res = requests.get('https://apexlegendsstatus.com/stats/')
        regex = re.search(
            'https:\/\/apexlegendsstatus.com\/profile\/uid\/(.*)\/(.*)"', res.text)
        if regex is None:
            raise Exception('Empty regex')

        platform = regex.group(1)
        uid = regex.group(2)
        apex_data = origin_api.apex_data(uid, platform)
        get_unknowns_keys(apex_data)

        print(i, f" {uid} | {platform} Done !")
    except Exception as e:
        print(i, ' ', e)
