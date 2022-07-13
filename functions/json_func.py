import json
from os.path import exists


def edit_data_json(data_arr, today):
    if exists('data.json'):
        with open('data.json', 'r', encoding='utf-8') as f:
            content = json.load(f)
            raw_content = content
            new_array = []
            data_index = 0

            while data_index < len(data_arr):
                found = False
                content_index = 0
                while content_index < len(raw_content):
                    if data_arr[data_index]['name'] == raw_content[content_index]['name']:
                        for data_key in data_arr[data_index]:
                            if not data_key == 'inserted':
                                content[content.index(raw_content[content_index])][data_key] = data_arr[data_index][data_key]
                        content[content.index(raw_content[content_index])]['updated'] = today
                        found = True
                        new_array.append(content[content.index(raw_content[content_index])])
                        break
                    content_index += 1
                if not found:
                    data_arr[data_index]['inserted'] = today
                    data_arr[data_index]['updated'] = today
                    new_array.append(data_arr[data_index])
                data_index += 1
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(new_array, f, ensure_ascii=False, indent=4)
        send_arr = content
    else:
        for data in data_arr:
            data['inserted'] = today
            data['updated'] = today
        with open('data.json', 'w', encoding='utf-8') as f:
            json.dump(data_arr, f, ensure_ascii=False, indent=4)
        send_arr = data_arr

    for entry in send_arr:
        counter = 0
        for other_entry in send_arr:
            if other_entry['name'] == entry['name']:
                counter += 1
        if counter > 1:
            send_arr.pop(send_arr.index(entry))

    return send_arr