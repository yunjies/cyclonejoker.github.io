import os, json, re

TEMPLATE_PATH = 'template.html'
IO_CONFIG_PATH = 'io_config.json'
CONTENT_MATCH = re.compile(r'window.location.href="https://cyclonejoker.xyz:([0-9]+)"')

def readConfig():
    data = {}
    with open(IO_CONFIG_PATH, encoding='utf-8') as jsonfile:
        data = json.load(jsonfile)
    return data

def readTemplate():
    data = {}
    with open(TEMPLATE_PATH, encoding='utf-8') as f:
        data = f.read()
    return data

def checkFileNeedUpdate(filepath, port):
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            r = CONTENT_MATCH.search(f.read())
            if r and r[1] == port:
                return False
    return True

def main():
    configs = readConfig()
    tempate = readTemplate()
    for config in configs:
        name = config['name']
        if not os.path.exists(name):
            os.mkdir(name)

        indexFilePath = name + '/index.html'
        if checkFileNeedUpdate(indexFilePath, config['port']):
            with open(indexFilePath, 'w', encoding='utf-8') as f:
                f.write(tempate.format(config['port']))

if __name__ == "__main__":
    main()
