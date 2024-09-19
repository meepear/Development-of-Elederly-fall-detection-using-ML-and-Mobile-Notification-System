import os
from twilio.rest import Client

# Access environment variables for Twilio credentials
account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

client = Client(account_sid, auth_token)

# Send SMS
message = client.messages.create(
    body="Hello World",    # The SMS body
    from_="+14156495637",  # Your Twilio phone number
    to="+660649769820"     # Recipient's phone number (ensure it's in E.164 format)
)

# Print the message SID (unique ID for the message)
print(message.sid)
