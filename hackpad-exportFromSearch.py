from hackpad import Hackpad
import datetime
import os
import paramiko
import re
import shutil
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

if config['consumer_key'] == '' or config['consumer_secret'] == '':
    print('Parameters missing. Please complete "parameters.yml" file')
    sys.exit()

hackpad = Hackpad(config['subdomain'], consumer_key=config['consumer_key'], consumer_secret=config['consumer_secret'])
keyword = sys.argv[1]
import2jingo = config['jingo']['import'] and (config['format'] == 'md')
tmpPath = tempfile.gettempdir()

if import2jingo:
    paramiko.util.log_to_file('%s/paramiko.log' % tmpPath)
    regex = re.compile(r'!\[(\w*)\]\([[a-zA-Z.-:-_]*\)', re.IGNORECASE)

print('=> Searching pads with following keyword : %s' % keyword)
params = {}
url = 'search?q=%s&start=%s&limit=%s' % (keyword, config['start'], config['limit'])
listPads = hackpad.do_api_request(url, 'GET', params)
nbPads = str(len(listPads))
print(nbPads + ' pad(s) retrieved')
print('')

format = "%Y-%m-%d_%H-%M-%S"
today = datetime.datetime.today()
today = today.strftime(format)
mPath = tmpPath + '/export-hackpad_'

if len(listPads) > 0:

    if import2jingo:
        transport = paramiko.Transport((config['jingo']['host'], config['jingo']['port']))
        transport.connect(username=config['jingo']['user'], password=config['jingo']['password'])
        sftp = paramiko.SFTPClient.from_transport(transport)

    for pad in listPads:

        padTitle = pad['title']
        padTitle = format_filename(padTitle)
        padId = pad['localPadId']

        print('==> Downloading Pad %s/%s: %s' % (str(listPads.index(pad) + 1), nbPads, padTitle))
        padUrl = 'pad/%s/content/%s.%s' % (padId, 'latest', config['format'])
        print('Fetching from : %s' % padUrl)
        content = hackpad.do_api_request(padUrl, 'GET', params)
        content = content.decode(config['encoding'])

        filePath = mPath + '%s_%s/%s' % (keyword, today, padTitle)
        fileFullPath = '%s/%s.%s' % (filePath, padTitle, config['format'])
        tempFullPath = '%s/%s.%s.tmp' % (filePath, padTitle, config['format'])

        os.makedirs(filePath, exist_ok=True)
        file = open(fileFullPath, "a")
        file.write(content)
        file.close()

        print('Searching images')
        file = open(fileFullPath, "r")
        ftmp = open(tempFullPath, "w")
        for line in file:

            result = re.search(r'!\[(\w*)\]\([[a-zA-Z.-:-_]*\)', line)
            if result:
                imgUrl = result.group().replace('![](', '')
                imgUrl = imgUrl.replace(')', '')
                imgName = imgUrl.split('/')
                pos = len(imgName) - 1
                img = imgName[pos]
                imgfile = urllib.request.urlopen(imgUrl)
                imgLocalUrl = filePath + '/' + img
                imgout = open(imgLocalUrl, 'wb')
                imgout.write(imgfile.read())
                imgout.close()
                print('  image downloaded : ' + img)

                if import2jingo:
                    remotefilepath = config['jingo']['imgDir'] + img
                    remoteImgUrl = config['jingo']['imgUrl'] + img
                    sftp.put(imgLocalUrl, remotefilepath)
                    print('    image uploaded on %s' % config['jingo']['host'])
                    ftmp.write(regex.sub('![image %s](%s)' % (img, remoteImgUrl), line))
                    print('    image url updated in %s file' % config['format'])
            else:
                ftmp.write(line)

        file.close()
        ftmp.close()
        os.remove(fileFullPath)
        shutil.move(tempFullPath, fileFullPath)

        if import2jingo:
            remotefilepath = config['jingo']['mdDir'] + padTitle + '.' + config['format']
            sftp.put(fileFullPath, remotefilepath)
            print('%s file uploaded on %s' % (config['format'], config['jingo']['host']))
        print('')

    if import2jingo:
        sftp.close()
        transport.close()

    print('')

print('=> export done')
