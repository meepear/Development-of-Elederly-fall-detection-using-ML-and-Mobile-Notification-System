from twilio.rest import Client

account_sid = 'AC0018846e8247afaeea6bbe8ad708f1e4'
auth_token = '5cde2eee24506e0e7c4628f5887b7796'
client = Client(account_sid, auth_token)

message = client.messages.create(
  from_='+13104398998',
  body='Hello World',
  to='+660649769820'
)

print(message.sid)