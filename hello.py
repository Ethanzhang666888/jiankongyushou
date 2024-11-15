from eth_account import Account
import os
import requests
from web3 import Web3

# Initialize a Web3 instance
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/TZC5IvT8TqaZxVb-YmPM8X1sMiFWEJZ3'))  # Replace with your Ethereum node URL

# Define your private key here
PRIVATE_KEY = os.getenv('PRIVATE_KEY')  # 从环境变量中获取私钥

# Define ACCOUNT using a private key
ACCOUNT = Account.from_key(PRIVATE_KEY)

# 使用私钥派生地址
derived_address = Account.from_key(PRIVATE_KEY).address
print(f"Derived address from PRIVATE_KEY: {derived_address}")
print(f"Configured ACCOUNT.address: {ACCOUNT.address}")

if derived_address != ACCOUNT.address:
    raise ValueError("PRIVATE_KEY does not match ACCOUNT.address!")


from eth_account.messages import encode_defunct

# 构建签名消息
message = f"{ACCOUNT.address}:eth_sendBundle"
message_encoded = encode_defunct(text=message)

# 使用私钥对消息签名
signature = w3.eth.account.sign_message(message_encoded, private_key=PRIVATE_KEY)

# Initialize headers dictionary
headers = {'Content-Type': 'application/json'}

# 打印签名头部信息
headers['X-Flashbots-Signature'] = f"{ACCOUNT.address}:{signature.signature.hex()}"
print(f"X-Flashbots-Signature: {headers['X-Flashbots-Signature']}")
