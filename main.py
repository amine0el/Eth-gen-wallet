from eth_keys import keys
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
api_key = "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"
import requests
import json
class Ethereum:
    def __init__(self, rpc_server):
        self.rpc_server = rpc_server
        self.headers = {
            'Content-Type': 'application/json',
        }
        self.server_state = self.test_server()
    def test_server(self):
        method = 'web3_clientVersion'
        params = []
        response = self._make_rpc_request(method, params)
        if "result" in response:
            return True
        else:
            return False
    def _make_rpc_request(self, method, params,getjson=True):
        payload = {
            'jsonrpc': '2.0',
            'id': 1,
            'method': method,
            'params': params,
        }
        try:
            response = requests.post(self.rpc_server, headers=self.headers, data=json.dumps(payload))
            if getjson:
                return response.json()
            return response
        except:
            return None
    def get_balance(self, eth_address):
        method = 'eth_getBalance'
        params = [eth_address, 'latest']
        response = self._make_rpc_request(method, params)
        if response is None:
            return None
        balance_wei = int(response['result'], 16)
        balance_eth = balance_wei / 1e18  # Convert Wei to Ether
        return balance_eth
rpc = Ethereum("https://eth-mainnet.g.alchemy.com/v2/i_AyXcC8sLn1ZVsJsCfqOHBV0kZ3I4K7")
rpc.test_server()
class SendGridEmailSender:
    def __init__(self):
        self.api_key = api_key
    def send_email(self, from_email, to_emails, subject, html_content):
        message = Mail(
            from_email=from_email,
            to_emails=to_emails,
            subject=subject,
            plain_text_content=" ",
            html_content=html_content
        )
        try:
            sg = SendGridAPIClient(api_key=self.api_key)
            response = sg.send(message)
            if response.status_code == 202:
                status = "Success"
            return status,""
        except Exception as e:
            print(str(e))
            return "Failed",str(e)
mail = SendGridEmailSender()
def generate_private_key():
    private_key_bytes = os.urandom(32)
    return keys.PrivateKey(private_key_bytes)
def count_successive_zeros(hex_string):
    max_zeros = 0
    current_zeros = 0
    for char in hex_string:
        if char == '0':
            current_zeros += 1
            max_zeros = max(max_zeros, current_zeros)
        else:
            current_zeros = 0
    return max_zeros
def  notify(message,count):
  mail.send_email("contact@xositron.com","got@xositron.com",f"Found One with {count}", message)
while True:
  # Generate a random private key
  private_key = generate_private_key()
  # Derive the corresponding public key
  public_key = private_key.public_key
  # Get the Ethereum address from the public key
  ethereum_address = public_key.to_checksum_address()
  count = count_successive_zeros(ethereum_address)
  balance = rpc.get_balance(str(ethereum_address))
  if balance==None:
      balance=-1
  if float(balance)> 0:
    notify(f"{balance}ETH| {ethereum_address} - {private_key}",count)
  if count > 2:
    with open(f"{count}_zeros.txt", "a") as fero:
      fero.write(f"\n{ethereum_address} - {private_key}")
  if count > 4:
    notify(f"{balance}ETH| {ethereum_address} - {private_key}",count)
  print(f"{balance}ETH| {count} | {ethereum_address} - {private_key}")
