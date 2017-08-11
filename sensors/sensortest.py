#!/usr/bin/env python

import requests
from requests.auth import HTTPBasicAuth
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import urllib3
import json
from time import sleep

__all__ = [
    'Icinga2ReqSensor'
]

class Icinga2ReqSensor():
  def setup(self):
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    self.r = None
    self.buffer = ''
    self.eventstream_type = 'StateChange'
    self.url = 'https://10.75.129.25:5665/v1'
    self.api_user = 'root'
    self.api_password = 'cb19f8e6ea64c501'
    self.cert = ''
    self.key = ''
    self.trigger_name = 'generic_event'
    self.trigger_pack = 'icinga2req'
    self.trigger_ref = '.'.join([self.trigger_pack, self.trigger_name])
    print('Icinga2ReqSensor initialized: ')
    
  def run(self):
    print('Setting up Icinga2 API connection')
    url = self.url + '/events?queue=icinga2req&types=' + self.eventstream_type + '&filter=event.state_type==1.0'
    print('Icinga2ReqSensor url: ', url)
    while True:
      try:
        if not self.cert:
          print('Icinga2ReqSensor: insecure')
          #Turns off SSL validation (Required for python pre-2.7.9)
          self.r = requests.post(url, auth=HTTPBasicAuth(self.api_user, self.api_password), stream=True, timeout=60,
            verify=False, hooks=dict(response=self.on_receive), headers={'Accept': 'application/json'})
        else:
          print('Icinga2ReqSensor: secure')
          #We have a cert, much more secure
          self.r = requests.post(url, auth=HTTPBasicAuth(self.api_user, self.api_password), stream=True, timeout=60,
            verify=self.cert, hooks=dict(response=self.on_receive), headers={'Accept': 'application/json'})
        print('Icinga2ReqSensor status_code: ', self.r.status_code)
      except:
        #This is not good..
        self.logger.info('Icinga2ReqSensor timed out... Retrying in 60s')
        sleep(60)
        continue
      if self.r.ok == False:
        print('Icinga2ReqSensor in failed connection state. Retrying in 60s')
        sleep(60)
      else:
        break

  def cleanup(self):
    if self.r:
      self.r.connection.close()

  def add_trigger(self, trigger):
    pass

  def update_trigger(self, trigger):
    pass

  def remove_trigger(self, trigger):
    pass

  def on_receive(self, r, *args, **kwargs):
    for line in r.iter_lines():
      linebuf = self.buffer + line
      self.buffer = ''
      linebuf = linebuf.replace('\n','')
      try:
        event = json.loads(linebuf)
        self.dispatch_trigger(event)
      except:
        self.buffer = linebuf

  def dispatch_trigger(self, event):
    ack = False
    address = ""
    address6 = ""
    var = {}
    if not 'service' in event:
      event['service'] = 'hostcheck'
    else:
      ack, address, address6, var = self.get_extra_info(event['host'], event['service'])
    payload = {}
    payload['service'] = event['service']
    payload['host'] = event['host']
    payload['access'] = { "address": address, "address6": address6}
    payload['state'] = event['state']
    payload['monitoring_source'] = 'icinga2'
    payload['output'] = event['check_result']['output']
    payload['timestamp'] = event['timestamp']
    payload['var'] = {}
    payload['var']['ack'] = ack
    if 'stack' in var:
      payload['var']['stack'] = var['stack']

    print('Processing event: ', payload)
    print('Dispatching trigger: ', self.trigger_ref)

  def get_extra_info(self,host,service):
    hostservice = host + "!" + service
    hostservice.replace(" ","%20")
    url = self.url + '/objects/services?service=' + hostservice 
    #return 0.0, "", "", {} 
    data = '{ "joins": [ "host.name", "host.address", "host.address6", "host.vars" ], "attrs": [ "acknowledgement" ] }'
    ok = False
    text = ""
    ok, text = self.call_api(url,data)
    if ok == False:
      #ok, retry once more....
      sleep(5)
      ok, text = self.call_api(url,data)
      if ok == False:
        #ok, tried this twice, treat this as a failure and return the default
        return 0.0, "", "", {}
    #and.., we probably have a good return result..
    j = json.loads(text)
    ack = False
    if j['results'][0]['attrs']['acknowledgement'] == 1.0:
      ack = True
    return ack, j['results'][0]['joins']['host']['address'], j['results'][0]['joins']['host']['address6'], j['results'][0]['joins']['host']['vars']

  def call_api(self,url,data):
    try:
      if not self.cert:
        #Pre python 2.7.9. Turns off SSL validation (Note: Ubuntu 14.04 ships with python 2.7.6)
        self.rapi = requests.post(url, auth=HTTPBasicAuth(self.api_user, self.api_password), stream=True, data=data, timeout=30,
          verify=False, headers={'Accept': 'application/json', 'X-HTTP-Method-Override': 'GET'})
      else:
        #We have a cert, much more secure
        self.rapi = requests.post(url, auth=HTTPBasicAuth(self.api_user, self.api_password), stream=True, data=data, timeout=30,
          verify=self.cert, headers={'Accept': 'application/json', 'X-HTTP-Method-Override': 'GET'})
    except:
      return False, ""
    return self.rapi.ok, self.rapi.text


req = Icinga2ReqSensor()
req.setup()
req.run()

