import json
import requests
import datetime as DT

now = DT.datetime.now()
today = DT.date.today()
week_ago = today - DT.timedelta(days=7)

def client():
    print('a')
    response = requests.post('http://127.0.0.1:8000/server_upd',{'Cur_ID':145,'Date':today,'Cur_OfficialRate':2.1555})
    print('b')
    response = json.loads(response.text)
    print(response['status'])

print(client())