import requests

url = 'https://notify-api.line.me/api/notify'
token = '4dVdQwJ1jzviBEilsZrRuZCTZDJpFaZjfGD4zgJWpyc'
header = {'Content-Type':'application/x-www-form-urlencoded',
          'Authorization':'Bearer ' + token}

msg = "Hello"
req = requests.post(url, headers=header, data={'message': msg})
print(req)