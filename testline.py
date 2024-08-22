import requests

url = 'https://notify-api.line.me/api/notify'
# Bot ส่วนตัว
# token = '4dVdQwJ1jzviBEilsZrRuZCTZDJpFaZjfGD4zgJWpyc'
# Fall_Down_Alert สำหรับกลุ่ม
token = '12zYABe0W2vdGWROK5xw09HuBOPX9vqDImeIaTWAr2Q'
header = {'Content-Type':'application/x-www-form-urlencoded',
          'Authorization':'Bearer ' + token}

msg = "Hello"
req = requests.post(url, headers=header, data={'message': msg})
print(req) 