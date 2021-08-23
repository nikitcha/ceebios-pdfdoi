import requests
import json
import time 

url = "http://localhost:3001/api/v1/"
file = "pdfs/KEEP COOL_BIOINSPIRATION_TRIBAN_vf.pdf"
config = 'config.json'
packet = {
            'file': (file, open(file, 'rb'), 'application/pdf'),
            'config': (config, open(config, 'rb'), 'application/json'),
        }
r = requests.post(url+'document', files=packet)
jid = r.text
finished = False

while not finished:
    time.sleep(0.5)
    status = requests.get(url+'queue/{}'.format(jid))
    status = json.loads(status.text)
    if 'json' in status:
        finished = True

res = requests.get(url+'json/'+jid)

with open('jsons/KEEP COOL_BIOINSPIRATION_TRIBAN_vf.json', mode='w',encoding='utf-8') as f:
    json.dump(res.json(),f,indent=4)    