from bs4 import BeautifulSoup
from hackpad import Hackpad
import markdown
import os
import re
import string
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

hackpad = Hackpad(config['subdomain'], consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'])


print("=> Retrieving all pads")
listPads = hackpad.do_api_request('pads/all', 'GET')
nbPads = str(len(listPads))
print(nbPads + ' pad(s) retrieved')
print('')

for padId in listPads:

    print('==> Downloading Pad %s/%s: %s' % (str(listPads.index(padId) + 1), nbPads, padId))

    padUrl = 'pad/%s/content/%s.%s' % (padId, 'latest', config['format'])
    params = {}
    print('Fetching from : %s' % padUrl)
    content = hackpad.do_api_request(padUrl, 'GET', params)
    content = content.decode(config['encoding'])

    filePath = '/tmp/export-hackpad-allPads/%s' % padId
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

    newFilePath = '/tmp/export-hackpad-allPads/%s' % title
    print('Renaming directory to ' + newFilePath)
    os.rename(filePath, newFilePath)

    print('')

print('=> export done')