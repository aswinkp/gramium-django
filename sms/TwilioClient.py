# coding=latin-1
from twilio.rest import TwilioRestClient

class TwilioClient:
    account = "ACf77bdabb559d9880ded6f082f11f4578"
    token = "a3abea2206d16a0551d0501f31728474"

    def createClient(self):
        client = None
        try:
            client = TwilioRestClient(self.account, self.token)
        except:
            print "Error while creating twilio client"
        return client

    def sendSMS(self, to, from_, body):
        client = self.createClient()
        try:
            client.messages.create(to=to, from_=from_,body=body)
            return_status = 0
        except Exception as e:
            print "Error while sending SMS"
            print e
            return_status = 1
        return return_status


if __name__ == "__main__":
    client = TwilioClient()
    client.sendSMS(to="+917358232971",  from_="(267) 433-0959", body="Hello There!")