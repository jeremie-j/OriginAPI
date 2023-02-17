import requests
import json

KEY = 'MUwcZXwlcWiE7bUUKi11'

platforms = ['PS4', 'PC', 'SWITCH', 'X1']

keys = {
    'legend': 'cdata2',
    'tracker0': 'cdata12',
    'tracker1': 'cdata14',
    'tracker2': 'cdata16',
    'badge0': 'cdata6',
    'badge1': 'cdata8',
    'badge2': 'cdata10',
    'frame': 'cdata4',
    'intro': 'cdata18',
    'pose': 'cdata5',
    'skin': 'cdata3',
}


def get_unknowns_keys(apex_data):
    uid = apex_data['uid']
    platform = apex_data['hardware']
    if uid is None:
        raise ValueError('Uid not found')
    a = requests.get(
        f'https://api.mozambiquehe.re/bridge?platform={platform}&uid={uid}&auth={KEY}')

    try:
        legend = a.json().get('legends').get('selected')
    except AttributeError:
        print(f"Not {platform} hardware")
        return

    with open('./scripts/scrap_mapping/mapping.json', 'r') as outfile:
        outfile_data = json.load(outfile)

        if outfile_data.get('legends') is None:
            outfile_data['legends'] = {}

        if outfile_data.get('badges') is None:
            outfile_data['badges'] = {}

    legend_name = legend.get('LegendName')
    game_info = legend.get('gameInfo')
    trackers = legend.get('data', [])
    skin = game_info.get('skin')
    frame = game_info.get('frame')
    intro = game_info.get('intro')
    pose = game_info.get('pose')
    badges = game_info.get('badges', [])

    if outfile_data['legends'].get(legend_name) is None:
        outfile_data['legends'] = {
            **outfile_data['legends'], legend_name: {
                'legend_id': None,
                'trackers': {},
                'skins': {},
                'intros': {},
                'poses': {},
                'frames': {},
                'badges': {}
            }}

    if outfile_data['legends'][legend_name]['legend_id'] is None:
        outfile_data['legends'][legend_name]['legend_id'] = int(
            apex_data[keys[f'legend']])
    elif outfile_data['legends'][legend_name]['legend_id'] != int(apex_data[keys[f'legend']]):
        print('Different legend id ?')

    for idx, tracker in enumerate(trackers):
        if tracker['key']:
            outfile_data['legends'][legend_name]['trackers'][
                int(apex_data[keys[f'tracker{idx}']])] = tracker['key']

    for idx, badge in enumerate(badges):
        if badge['name'] is not None:
            if badge['category'] == "Account Badges" and badge['name']:
                outfile_data['badges'][int(apex_data[keys[f'badge{idx}']])
                                       ] = badge['name']
            elif badge['category'] == legend_name and badge['name']:
                outfile_data['legends'][legend_name]['badges'][
                    int(apex_data[keys[f'badge{idx}']])] = badge['name']
            else:
                print('unknow category :', badge['category'])
    if skin:
        outfile_data['legends'][legend_name]['skins'][int(
            apex_data[keys[f'skin']])] = skin

    if intro:
        outfile_data['legends'][legend_name]['intros'][int(
            apex_data[keys[f'intro']])] = intro

    if pose:
        outfile_data['legends'][legend_name]['poses'][int(
            apex_data[keys[f'pose']])] = pose

    if frame:
        outfile_data['legends'][legend_name]['frames'][int(
            apex_data[keys[f'frame']])] = frame

    with open('./scripts/scrap_mapping/mapping.json', 'w') as outfile:
        json.dump(outfile_data, outfile)
