api_key = '0792ed4148e32da9b6e3a7d9d61a8f5b'
api_secret = '923fd6a3ad7e83a7af1105083de5ae1c'

from mailjet_rest import Client
mailjet = Client(auth=(api_key, api_secret), version='v3.1')


data = {
  'Messages': [
    {
      "From": {
        "Email": "admin@arpansahu.me",
        "Name": "arpan"
      },
      "To": [
        {
          "Email": "arpanrocks95@gmail.com",
          "Name": "arpan"
        }
      ],
      "Subject": "Greetings from Mailjet.",
      "TextPart": "My first Mailjet email",
      "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
      "CustomID": "AppGettingStartedTest"
    }
  ]
}
result = mailjet.send.create(data=data)
print (type(result.status_code))
print (result.json())
