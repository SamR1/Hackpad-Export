# Hackpad-Export
Script to export pads and associated images :
- from search on Hackpad.com
- all pads associated to the user  
  
If you use [Jingo](https://github.com/claudioc/jingo), you can import **.md** files to your self-hosted Jingo.  
  
## Prerequisites :
- Python 3 (tested with 3.5)
- PyYAML: http://pyyaml.org/
- for **hackpad-exportAllPads.py** :
    - [BeautifulSoup4](https://pypi.python.org/pypi/beautifulsoup4)
    - [Python-Markdown](https://pythonhosted.org/Markdown/)
- for **hackpad-exportFromSearch.py** :
    - [Paramiko](http://www.paramiko.org/)

## How-To :
* update the parameter file :
    * **consumer_key** and **consumer_secret**: see your API key in your [account settings](https://hackpad.com/ep/account/settings/) 
    * **subdomain**: mysubdomain for http://mysubdomain.hackpad.com, leave empty if you're not using a subdomain
    * **format**: 'md', 'html' or 'txt'
    * for Jingo (only for **hackpad-exportFromSearch.py**) :
        * **import** : _true_ to activate import in Jingo (Note : if only the **md** format is configured)
        * parameters to connect to the server where Jingo is hosted
        * directories where files are stored (on my server, **md** files and **images** are not in the same directory)
* run the script :
    * to export pads resulting from search :  
    ```
    $ python hackpad-exportFromSearch.py keyword
    ```
    * to export all Pads :  
    ```
    $ python hackpad-exportAllPads.py
    ```
All pads for which you have access are exported in **temp** directory with images (and imported in Jingo, if configured).  
_Be aware of Hackpad.com API parameters (the number of returned results has to be adjusted in the parameter file (no pagination system))_

## Sources
**hackpad.py** : light version of [Falicon/Python-Hackpad-API](https://github.com/Falicon/Python-Hackpad-API)
