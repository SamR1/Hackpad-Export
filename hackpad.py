import sys

from requests_oauthlib import OAuth1Session
from urllib.parse import urljoin

class Hackpad(object):
  def __init__(self, sub_domain='', consumer_key='', consumer_secret=''):
    self.sub_domain = sub_domain
    self.consumer_key = consumer_key
    self.consumer_secret = consumer_secret
    return

  def get_pad_content(self, padId, revision='latest', response_format='txt', asUser=''):
    api_link = 'pad/%s/content/%s.%s' % (padId, revision, response_format)
    params = {}
    if asUser != '':
      params['asUser'] = asUser
    return self.do_api_request(api_link, 'GET', params)

  def search_for_pads(self, q='', start=0, limit=10, asUser=''):
    api_link = 'search'
    params = {'q':q, 'start':start, 'limit':limit}
    if asUser != '':
      params['asUser'] = asUser
    return self.do_api_request(api_link, 'GET', params)

  def list_all(self):
    api_link = 'pads/all'
    return self.do_api_request(api_link, 'GET')

  def do_api_request(self, path, method, post_data={}, body='', content_type=None):
    method = method.upper()
    hackpad = {}
    try:
      if self.sub_domain:
        path = urljoin('https://%s.hackpad.com/api/1.0/' % self.sub_domain, path)
      else:
        path = urljoin('https://hackpad.com/api/1.0/', path)

      params = {
        'client_key': self.consumer_key,
        'client_secret': self.consumer_secret
      }

      headers = {}
      if content_type:
        headers['content-type'] = content_type

      for key in post_data.keys():
        params[key] = post_data[key]

      hackpad_api = OAuth1Session(**params)

      if method == 'POST':
        r = hackpad_api.post(path, data=body, headers=headers)
        hackpad = r.json()
      else:
        r = hackpad_api.get(path, headers=headers)

        try:
            hackpad = r.json()
        except:
            hackpad = r.content
    except:
      print(sys.exc_info()[0])

    return hackpad
