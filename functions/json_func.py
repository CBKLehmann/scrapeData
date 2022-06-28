import json
from os.path import exists


def edit_data_json(data_arr, today):
    if exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            content = json.load(f)
            raw_content = content
            content_index = 0
            while content_index < len(raw_content):
                data_index = 0
                while data_index < len(data_arr):
                    if data_arr[data_index]['name'] == raw_content[content_index]['name']:
                        for data_key in data_arr[data_index]:
                            if not data_key == 'inserted':
                                content[content.index(raw_content[content_index])][data_key] = data_arr[data_index][data_key]
                        content[content.index(raw_content[content_index])]['updated'] = today
                    data_index += 1
                content_index += 1
    else:
        for data in data_arr:
            data['inserted'] = today
            data['updated'] = today
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data_arr, f, ensure_ascii=False, indent=4)
