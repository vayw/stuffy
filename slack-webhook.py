#!/bin/env python3


import json
import urllib.request

class slackWebHook:

  def __init__(self, url="", name="pybot", icon = "", channel = ""):
    self.url = url
    self.name = name
    self.icon = icon
    self.channel = channel

  def send(self, payload):
    """
    Send payload to slack API
    """
    msg = {'username': self.name, "channel": self.channel, "icon_emoji": self.icon, 'text': payload}
    payload_json = json.dumps(msg)
    params = json.dumps(msg).encode('utf8')
    req = urllib.request.Request(self.url, data=params, headers={'content-type': 'application/json'})
    response = urllib.request.urlopen(req)
    return (response.msg, response.code)
