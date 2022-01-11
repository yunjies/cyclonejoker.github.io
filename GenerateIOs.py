import os, json

TEMPLATE_PATH = 'template.html'
IO_CONFIG_PATH = 'io_config.json'

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

def main():
    configs = readConfig()
    tempate = readTemplate()
    for config in configs:
        name = config['name']
        if not os.path.exists(name):
            os.mkdir(name)

        indexFilePath = name + '/index.html'
        if os.path.exists(indexFilePath):
            os.remove(indexFilePath)
        
        with open(indexFilePath, 'w', encoding='utf-8') as f:
            f.write(tempate.format(config['port']))

if __name__ == "__main__":
    main()
