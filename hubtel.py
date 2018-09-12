"""
Python package for Hubtel's Payment API.
github.com/mcroni/hubtel

Usage:
# >>> import Hubtel
# >>> p = Hubtel("username","password","merchant")
# >>> request = p.receive("kojo mcroni","027180861x","kojo_mcroni@xxx.com","tigo-gh",5,"http://xxxx.com/callback","for lola rae",fees=True,cl_reg)
# >>> print(request)

# >>> check = p.trans_status(hubtel_trans="c05786985b4a48f5a786321268e10537")
# >>> print(check)

:copyright: (c) 2017
by Joey Daniel Darko
@kojo_mcroni
joeydnanieldarko@gmail.com

:license: MIT, see LICENSE for more details.
"""


import requests, base64
class Hubtel:
    def __init__(self,username,password,merchantId):
        self.base_url = "https://api.hubtel.com/v1/merchantaccount/"
        self.username = username
        self.password = password
        self.merchant_id = merchantId
        usrPass = "{0}:{1}".format(self.username,self.password)
        auth_byte = usrPass.encode('utf-8')
        self.basic = str(base64.b64encode(auth_byte))[2:-1]
        self.headers = {'Authorization': 'Basic {0}'.format(self.basic)}
        self.items = []
        print(self.basic)

    def receive(self,name,number,email,channel,amount,callback,description,cl_ref,fees,sec_callback="",token=""):
        """This enables you to send money to a mobile money wallet. You need to have money in your Hubtel Prepaid Balance
        to be able to use this functionality. You can fund your Prepaid Balance by transfering money from your Available
        Balance to your Prepaid Balance or you can fund your Prepaid Balance at any of Hubtel's partner banks"""
        base_url = "https://api.hubtel.com/v1/merchantaccount/merchants/{0}/receive/mobilemoney".format(self.merchant_id)
        payload = {
            "CustomerName": name,"CustomerMsisdn": number,"CustomerEmail": email,"Channel": channel,"Amount": amount,
            "PrimaryCallbackUrl": callback,"SecondaryCallbackUrl": sec_callback,"Description": description,
            "ClientReference": cl_ref,"Token": token,"FeesOnCustomer": fees}
        try:
            r = requests.post(base_url, headers=self.headers,data=payload)
            return r.json()
        except Exception as e:
            print(e)

    def send(self,name,number,email,channel,amount,callback,description,cl_ref,sec_callback=""):
        """A send money request is asynchronous for both Vodafone Cash and Airtel Money, hence you should implement a
        callback to confirm the status of a transaction on these two networks. You do not have to implement a callback
        for MTN MoMo and Tigo Cash. """

        base_url = "https://api.hubtel.com/v1/merchantaccount/merchants/{0}/send/mobilemoney".format(self.merchant_id)
        payload = {
            "RecipientName": name,"RecipientMsisdn": number,"CustomerEmail": email,"Channel": channel,"Amount": amount,
            "PrimaryCallbackUrl": callback,"SecondaryCallbackUrl": sec_callback,"Description": description,
            "ClientReference": cl_ref}
        try:
            r = requests.post(base_url, headers=self.headers, data=payload)
            return r.json()
        except Exception as e:
            print(e)

    def trans_status(self,invoice=None,network_trans=None,hubtel_trans=None):
        """This allows a merchant to check for the current status of a transaction by providing a transaction identifier.
        A query to this endpoint returns the status of a mobile money or an online checkout transaction along with
        extra transaction data."""
        base_url = "https://api.hubtel.com/v1/merchantaccount/merchants/{0}/transactions/" \
                   "status?invoiceToken={1}&networkTransactionId={2}&hubtelTransactionId={3}".format(self.merchant_id,
                   invoice,network_trans,hubtel_trans)

        try:
            r = requests.get(base_url, headers=self.headers)
            return r.json()
        except Exception as e:
            print(e)

    def refund(self,trans_id,reason,cl_ref,description,amount,full):
        """This allows a merchant to refund a mobile money wallet in part or in full. A request to this endpoint will
         move the transaction amount from your Merchant Account into the customer's mobile money wallet.."""
        base_url = "https://api.hubtel.com/v1/merchantaccount/merchants/{0}/transactions/refund".format(self.merchant_id)
        payload = {
          "TransactionId": trans_id,
          "Reason":reason,
          "ClientReference": cl_ref,
          "Description": description,
          "Amount": amount,
          "Full": full
        }
        try:
            r = requests.post(base_url, headers=self.headers, data=payload)
            return r.json()
        except Exception as e:
            print(e)

    def smc(self,channel,amount):
        """Used to determine the charge of a send payment from a merchant account into mobile money wallet. """
        base_url = "https://api.hubtel.com/v1/merchantaccount/merchants/{0}/charges/mobile/send".format(self.merchant_id)
        payload = {
          "channel":channel,
            "amount":amount
        }
        try:
            r = requests.post(base_url, headers=self.headers,data=payload)
            return r.json()
        except Exception as e:

            print(e)

    def confirm(self,name,number,email,channel,amount,reference):
        """confirm the receipt of a payment"""
        base_url = "https://api.hubtel.com/v1/merchantaccount/merchants/{0}/confirm/mobilemoney".format(self.merchant_id)
        payload = {
          "CustomerName": "string",
          "CustomerMsisdn": "string",
          "CustomerEmail": "string",
          "Channel": "string",
          "Amount": 0,
          "PaymentReferenceCode": "string"
        }
        payload = {
            "CustomerName": name, "CustomerMsisdn": number, "CustomerEmail": email, "Channel": channel,
            "Amount": amount,"PaymentReferenceCode": reference}
        try:
            r = requests.post(base_url, headers=self.headers, data=payload)
            return r.json()
        except Exception as e:
            print(e)

    def add_to_items(self, name, quantity, unit_price, item_image=None):
        """use this to add items to your cart when using.The invoice items object specifies the list of items to display
         on the invoice page."""
        self.items.append({
            "name": str(name),
            "quantity": int(quantity),
            "unitPrice": float(unit_price),
            "itemImageUrl": item_image
        })

    def clear_items(self):
        """clear all items in the list"""
        self.items.clear()

    def create_invoice(self,total,description,callback,return_url,logo,cl_ref,cancel_url=None):
        """this is for receiving payments thru the means of CC and DC.The invoice object specifies the list of items to
         display on the invoice page.When the invoice is created, your application receives an invoice token and a
         checkout URL for a customer to make payment."""
        base_url = "https://api.hubtel.com/v2/pos/onlinecheckout"
        payload = {
              "items": self.items,"totalAmount": total,"description": description, "callbackUrl": callback,"returnUrl": return_url,
              "merchantBusinessLogoUrl": logo,"merchantAccountNumber": self.merchant_id,"cancellationUrl": cancel_url,"clientReference": cl_ref
        }
        try:
            r = requests.post(base_url, headers=self.headers, data=payload)
            print("creating invoice")
            return r
        except Exception as e:
            print("got error")
            print(e)



# hub = Hubtel("dtajuwmo","xgvbtkvc","HMxxx07180001")
# test = hub.receive("sebas","0277402242","mcroni@gmail.com","tigo-gh",amount=2,callback="http://localhost:8000/callback",
#                                   description="contributinos to Agripool",cl_ref="2323GHs",fees=True)
# print(test)
# hub.add_to_items("mcroni",2,2.0)
# hub.add_to_items("love",2,2.0)
# print(type(hub.items))
# a = hub.create_invoice(40,"love","http://mcroni.com/","http://callbac.com/","http://logo.com","123")
# print(a)

# cas = hub.confirm("mcroni",amount=10,number="0271808617",email="kojo@kojo.com",channel="tigo-gh",reference="f46ce1b412df4009a0b8c995e87adad2")
# print(cas)
# check = hub.trans_status(invoice="2292647")
# print(check)
# fd="f46ce1b412df4009a0b8c995e87adad2"
# externalTransactionId= '2292647',
# a = hub.receive("kojo mcroni","0271808617","kojo_mcroni@xxx.com","tigo-gh",5,"http://xxxx.com/callback","for lola rae","for kojo",True)
# print(a)
