import os
import json
import requests

def get_json_files(directory):
    """获取指定目录下的所有JSON文件路径"""
    return [os.path.join(directory, f) for f in os.listdir(directory) if f.endswith('.json')]

def read_json_file(file_path):
    """读取并解析JSON文件"""
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def write_json_file(file_path, data):
    """将数据写回JSON文件"""
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, indent=4)

def check_url_exists(url):
    """检测URL中的文件是否存在"""
    try:
        response = requests.head(url, allow_redirects=True)
        if response.status_code == 200:
            if response.headers['Content-Type'] == 'application/x-7z-compressed':
                return True
        elif response.status_code == 200 and response.headers.get('Content-Type') == 'application/json':
            return False
            
    except requests.RequestException:
        return False

def main(directory):
    json_files = get_json_files(directory)
    for json_file in json_files:
        data = read_json_file(json_file)
        updated = False
        for key, value in data.items():
            if isinstance(value, dict) and 'url' in value:
                url = value['url']
                if not check_url_exists(url):
                    value['status'] = False
                    updated = True
                else:
                    value['status'] = True
                    updated = True
        if updated:
            write_json_file(json_file, data)

if __name__ == "__main__":
    directory = os.path.dirname(os.path.abspath(__file__))
    main(directory)