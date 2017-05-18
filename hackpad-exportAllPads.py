from bs4 import BeautifulSoup
from hackpad import Hackpad
import datetime
import markdown
import os
import re
import string
import sys
import urllib
import yaml


def format_filename(s):
    valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in s if c in valid_chars)
    filename = filename.replace(' ', '_')
    return filename

with open("parameters.yml", 'r') as stream:
    try:
        config = yaml.load(stream)
    except yaml.YAMLError as e:
        print(e)

if config['consumer_key'] == '' or config['consumer_secret'] == '':
    print('Parameters missing. Please complete "parameters.yml" file')
    sys.exit()

hackpad = Hackpad(config['subdomain'], consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'])


print("=> Retrieving all pads")
listPads = hackpad.do_api_request('pads/all', 'GET')
nbPads = str(len(listPads))
print(nbPads + ' pad(s) retrieved')
print('')

format = "%Y-%m-%d_%H-%M-%S"
today = datetime.datetime.today()
mainPath = '/tmp/export-hackpad-allPads_' + today.strftime(format) + '/'

for padId in listPads:

    print('==> Downloading Pad %s/%s: %s' % (str(listPads.index(padId) + 1), nbPads, padId))

    padUrl = 'pad/%s/content/%s.%s' % (padId, 'latest', config['format'])
    params = {}
    print('Fetching from : %s' % padUrl)
    content = hackpad.do_api_request(padUrl, 'GET', params)
    content = content.decode(config['encoding'])

    filePath = mainPath + '%s' % padId
    fileFullPath = '%s/%s.%s' % (filePath, padId, 'md')

    os.makedirs(filePath, exist_ok=True)
    file = open(fileFullPath, "a")
    file.write(content)
    file.close()

    firstline = True

    print('Searching images')
    file = open(fileFullPath, "r")
    for line in file:

        if firstline:
            title = markdown.markdown(line)
            title = BeautifulSoup(title, "html.parser").text
            title = format_filename(title)
        firstline = False

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
            print('  image downloaded : ' + img )

    file.close()

    newFilePath = mainPath + '%s' % title
    print('Renaming directory to ' + newFilePath)
    try:
        os.rename(filePath, newFilePath)
    except Exception as e:
        print('ERROR during directory renaming ' + str(e))
        pass
    print('')

print('=> export done')