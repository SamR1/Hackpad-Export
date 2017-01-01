# Hackpad-Export
Script to export pads and associated images :
- from search on Hackpad.com
- all pads associated to the user

## Prerequisites :
- Python 3 (tested with 3.5)
- Python library PyYAML: http://pyyaml.org/
- for "allPads" script :
    - [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
    - [Python-Markdown](https://pythonhosted.org/Markdown/)

## How-To :
* update the parameter file :
    * consumer_key and consumer_secret: see your API key in your [account settings](https://hackpad.com/ep/account/settings/) 
    * subdomain: mysubdomain for http://mysubdomain.hackpad.com, leave empty if you're not using a subdomain
    * format: 'md', 'html' or 'txt'
* run the script :

    * to export pads resulting from search :
```
$ python hackpad-exportFromSearch.py keyword
```
    * to export all Pads : 
```
$ python hackpad-exportAllPads
```   

All pads for which you have access are exported in **temp** directory with images.
_Be aware of Hackpad.com API parameters (the number of returned results has to be adjusted in the parameter file (no pagination system))_

## Sources
**hackpad.py** : light version of [Falicon/Python-Hackpad-API](https://github.com/Falicon/Python-Hackpad-API)
