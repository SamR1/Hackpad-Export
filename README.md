# Hackpad-Export
Script to export pads and associated images, from search on Hackpad.com

## Prerequisites :
- Python 3 (tested with 3.5)
- Python library PyYAML: http://pyyaml.org/

## How-To :
* configure the parameter file
    * consumer_key and consumer_secret: see your API key in your [account settings](https://hackpad.com/ep/account/settings/) 
    * subdomain: mysubdomain for http://mysubdomain.hackpad.com, leave empty if you're not using a subdomain
    * format: 'md', 'html' or 'txt'
* run the script :
```
$ python hackpad-exportFromSearch.py keyword
```

All pads for which you have access are exported in **temp** directory with images.

## Sources
**hackpad.py** : light version of [Falicon/Python-Hackpad-API](https://github.com/Falicon/Python-Hackpad-API)
