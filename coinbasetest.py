from coinbase.wallet.client import Client

api_key = 'of71uB7fEysCzQMp'
api_secret = 'k2cvJr3UuUhXc2pKPE2I6IV5cxQ7wVV0'
SANDBOX_URL = 'https://api.sandbox.coinbase.com'

import pdb; pdb.set_trace()

client = Client(
    api_key,
    api_secret,
    base_api_uri=SANDBOX_URL)

accounts = client.get_accounts()

print('accounts:', accounts)

for account in accounts.data:
  balance = account.balance
  print("%s: %s %s" % (account.name, balance.amount, balance.currency))
  print(account.get_transactions())

account = client.create_account(name="New Wallet")
balance = account.balance
print("%s: %s %s" % (account.name, balance.amount, balance.currency))

primary_account = client.get_primary_account()
address = account.create_address()

primary_account.send_money(
    to=address.address,
    amount='0.01',
    currency='BTC',
    description='For being awesome!')

print(primary_account.get_transactions()[-1])

primary_account.refresh()
balance = primary_account.balance
print("%s: %s %s" % (primary_account.name, balance.amount, balance.currency))
