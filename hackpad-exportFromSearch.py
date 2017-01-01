from hackpad import Hackpad
import os
import re
import string
import sys
import tempfile
import urllib
import yaml


def format_filename(s):
    # https://gist.github.com/seanh/93666
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')
    return filename


with open("parameters.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as e:
        print(e)


hackpad = Hackpad(config['subdomain'], consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'])
keyword = sys.argv[1]

print('=> Searching pads with following keyword : %s' % keyword)
params = {}
url = 'search?q=%s&start=%s&limit=%s' % (keyword, config['start'], config['limit'])
listPads = hackpad.do_api_request(url, 'GET', params)
nbPads = str(len(listPads))
print(nbPads + ' pad(s) retrieved')
print('')


for pad in listPads:

    padTitle = pad['title']
    padTitle = format_filename(padTitle)
    padId = pad['localPadId']

    print('==> Downloading Pad %s/%s: %s' % (str(listPads.index(pad) + 1), nbPads, padTitle))
    padUrl = 'pad/%s/content/%s.%s' % (padId, 'latest', config['format'])
    print('Fetching from : %s' % padUrl)
    content = hackpad.do_api_request(padUrl, 'GET', params)
    content = content.decode(config['encoding'])

    tmpPath = tempfile.gettempdir()
    filePath = '%s/export-hackpad/%s' % (tmpPath, padTitle)
    fileFullPath = '%s/%s.%s' % (filePath, padTitle, 'md')

    os.makedirs(filePath, exist_ok=True)
    file = open(fileFullPath, "a")
    file.write(content)
    file.close()

    print('Searching images')
    file = open(fileFullPath, "r")
    for line in file:

        result = re.search(r'!\[(\w*)\]\([[a-zA-Z.-:-_]*\)', line)
        if result:
            imgUrl = result.group().replace('![](', '')
            imgUrl = imgUrl.replace(')', '')
            imgName = imgUrl.split('/')
            pos = len(imgName) - 1
            img = imgName[pos]
            imgfile = urllib.request.urlopen(imgUrl)
            imgout = open(filePath + '/' + img, 'wb')
            imgout.write(imgfile.read())
            imgout.close()
            print('  image downloaded : ' + img)

    file.close()

    print('')

print('=> export done')
