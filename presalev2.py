import time
import logging
from web3 import Web3
from eth_account import Account
from web3.middleware import ExtraDataToPOAMiddleware
import requests
import os
from eth_account.messages import encode_defunct

# 配置日志
logging.basicConfig(level=logging.INFO)

# 连接到Sepolia
w3 = Web3(Web3.HTTPProvider('https://eth-sepolia.g.alchemy.com/v2/TZC5IvT8TqaZxVb-YmPM8X1sMiFWEJZ3'))
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)  # 用于处理Sepolia的PoA机制

# 配置合约和账户信息
CONTRACT_ADDRESS = '0x5E2E5a65Ff5d8586762e7313dc4e1dBe3D095adC'
PRIVATE_KEY = os.getenv('PRIVATE_KEY')  # 从环境变量中获取私钥
ACCOUNT = Account.from_key(PRIVATE_KEY)
CONTRACT_ABI = [
        {
            "type": "constructor",
            "inputs": [],
            "stateMutability": "nonpayable"
        },
        {
            "type": "function",
            "name": "approve",
            "inputs": [
                {
                    "name": "to",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable"
        },
        {
            "type": "function",
            "name": "balanceOf",
            "inputs": [
                {
                    "name": "owner",
                    "type": "address",
                    "internalType": "address"
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "enablePresale",
            "inputs": [],
            "outputs": [],
            "stateMutability": "nonpayable"
        },
        {
            "type": "function",
            "name": "getApproved",
            "inputs": [
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "address"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "isApprovedForAll",
            "inputs": [
                {
                    "name": "owner",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "operator",
                    "type": "address",
                    "internalType": "address"
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "bool",
                    "internalType": "bool"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "isPresaleActive",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "bool",
                    "internalType": "bool"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "name",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "string",
                    "internalType": "string"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "ownerOf",
            "inputs": [
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "address",
                    "internalType": "address"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "presale",
            "inputs": [
                {
                    "name": "amount",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "outputs": [],
            "stateMutability": "payable"
        },
        {
            "type": "function",
            "name": "safeTransferFrom",
            "inputs": [
                {
                    "name": "from",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "to",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable"
        },
        {
            "type": "function",
            "name": "safeTransferFrom",
            "inputs": [
                {
                    "name": "from",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "to",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                },
                {
                    "name": "data",
                    "type": "bytes",
                    "internalType": "bytes"
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable"
        },
        {
            "type": "function",
            "name": "setApprovalForAll",
            "inputs": [
                {
                    "name": "operator",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "approved",
                    "type": "bool",
                    "internalType": "bool"
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable"
        },
        {
            "type": "function",
            "name": "supportsInterface",
            "inputs": [
                {
                    "name": "interfaceId",
                    "type": "bytes4",
                    "internalType": "bytes4"
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "bool",
                    "internalType": "bool"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "symbol",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "string",
                    "internalType": "string"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "tokenURI",
            "inputs": [
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "outputs": [
                {
                    "name": "",
                    "type": "string",
                    "internalType": "string"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "totalSupply",
            "inputs": [],
            "outputs": [
                {
                    "name": "",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "stateMutability": "view"
        },
        {
            "type": "function",
            "name": "transferFrom",
            "inputs": [
                {
                    "name": "from",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "to",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ],
            "outputs": [],
            "stateMutability": "nonpayable"
        },
        {
            "type": "event",
            "name": "Approval",
            "inputs": [
                {
                    "name": "owner",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address"
                },
                {
                    "name": "approved",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "indexed": True,
                    "internalType": "uint256"
                }
            ],
            "anonymous": False
        },
        {
            "type": "event",
            "name": "ApprovalForAll",
            "inputs": [
                {
                    "name": "owner",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address"
                },
                {
                    "name": "operator",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address"
                },
                {
                    "name": "approved",
                    "type": "bool",
                    "indexed": False,
                    "internalType": "bool"
                }
            ],
            "anonymous": False
        },
        {
            "type": "event",
            "name": "Transfer",
            "inputs": [
                {
                    "name": "from",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address"
                },
                {
                    "name": "to",
                    "type": "address",
                    "indexed": True,
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "indexed": True,
                    "internalType": "uint256"
                }
            ],
            "anonymous": False
        },
        {
            "type": "error",
            "name": "ERC721IncorrectOwner",
            "inputs": [
                {
                    "name": "sender",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                },
                {
                    "name": "owner",
                    "type": "address",
                    "internalType": "address"
                }
            ]
        },
        {
            "type": "error",
            "name": "ERC721InsufficientApproval",
            "inputs": [
                {
                    "name": "operator",
                    "type": "address",
                    "internalType": "address"
                },
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ]
        },
        {
            "type": "error",
            "name": "ERC721InvalidApprover",
            "inputs": [
                {
                    "name": "approver",
                    "type": "address",
                    "internalType": "address"
                }
            ]
        },
        {
            "type": "error",
            "name": "ERC721InvalidOperator",
            "inputs": [
                {
                    "name": "operator",
                    "type": "address",
                    "internalType": "address"
                }
            ]
        },
        {
            "type": "error",
            "name": "ERC721InvalidOwner",
            "inputs": [
                {
                    "name": "owner",
                    "type": "address",
                    "internalType": "address"
                }
            ]
        },
        {
            "type": "error",
            "name": "ERC721InvalidReceiver",
            "inputs": [
                {
                    "name": "receiver",
                    "type": "address",
                    "internalType": "address"
                }
            ]
        },
        {
            "type": "error",
            "name": "ERC721InvalidSender",
            "inputs": [
                {
                    "name": "sender",
                    "type": "address",
                    "internalType": "address"
                }
            ]
        },
        {
            "type": "error",
            "name": "ERC721NonexistentToken",
            "inputs": [
                {
                    "name": "tokenId",
                    "type": "uint256",
                    "internalType": "uint256"
                }
            ]
        }
    ]

contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=CONTRACT_ABI)

# 1. 监听MemPool中的 enablePresale 交易
def listen_for_enable_presale():
    logging.info("Listening for enablePresale transactions...")
    filter = w3.eth.filter('pending')
    while True:
        for tx_hash in filter.get_new_entries():
            try:
                tx = w3.eth.get_transaction(tx_hash)
                if tx['to'] == CONTRACT_ADDRESS and contract.decode_function_input(tx.input)[0].fn_name == 'enablePresale':
                    logging.info(f"Detected enablePresale transaction: {tx_hash.hex()}")
                    # 构建和签名一个新的 enablePresale 交易,签名 presale(2) 交易
                    enable_presale_tx = contract.functions.enablePresale().build_transaction({
                        'from': ACCOUNT.address,
                        'nonce': w3.eth.get_transaction_count(ACCOUNT.address),
                        'gas': 200000,
                        'gasPrice': w3.eth.gas_price
                    })
                    signed_enable_tx = w3.eth.account.sign_transaction(enable_presale_tx, PRIVATE_KEY)
                    return signed_enable_tx
            except Exception as e:
                logging.error(f"Error while listening for transactions: {e}")
                time.sleep(1)
        time.sleep(5)

# 2. 签名 presale(2) 交易
def create_presale_transaction():
    logging.info("Creating presale transaction...")
    presale_tx = contract.functions.presale(2).build_transaction({
        'from': ACCOUNT.address,
        'nonce': w3.eth.get_transaction_count(ACCOUNT.address),
        'gas': 200000,
        'gasPrice': w3.eth.gas_price
    })
    signed_presale_tx = w3.eth.account.sign_transaction(presale_tx, PRIVATE_KEY)
    return signed_presale_tx

# 3. 捆绑交易并发送
def send_bundle(signed_enable_tx, signed_presale_tx):
    logging.info("Bundling and sending transactions...")

    # 构建交易捆绑
    bundle = [
        {"signed_transaction": signed_enable_tx.raw_transaction.hex()},
        {"signed_transaction": signed_presale_tx.raw_transaction.hex()}
    ]

    # Flashbots请求参数
    payload = {
        "jsonrpc": "2.0",
        "method": "eth_sendBundle",
        "params": [{
            "txs": [tx["signed_transaction"] for tx in bundle],
            "blockNumber": hex(w3.eth.block_number + 1),  # 指定有效区块号
            # 如果需要，也可以加入其他可选参数，例如 minTimestamp、maxTimestamp 等
        }],
        "id": 1
    }
    headers = {'Content-Type': 'application/json'}
    

    # 使用私钥对请求签名，生成 X-Flashbots-Signature 头
    message = f"{ACCOUNT.address}:eth_sendBundle"
    message_encoded = encode_defunct(text=message)  # 正确构建消息格式
    signature = w3.eth.account.sign_message(message_encoded, private_key=PRIVATE_KEY)
    headers['X-Flashbots-Signature'] = f"{ACCOUNT.address}:{signature.signature.hex()}"

    # 打印签名调试信息
    logging.debug(f"X-Flashbots-Signature: {headers['X-Flashbots-Signature']}")
    
    # 发送请求到Flashbots relay
    response = requests.post('https://relay-sepolia.flashbots.net', json=payload, headers=headers)
    
    # 打印原始响应内容
    logging.debug(f"Raw response content: {response.text}")
    
    try:
        result = response.json()
    except Exception as e:
        logging.error(f"Failed to parse JSON response: {e}")
        return

    if 'result' in result:
        logging.info(f"Bundle sent successfully. Bundle hash: {result['result']}")
    else:
        logging.error(f"Failed to send bundle: {result}")

# 主函数
def main():
    signed_enable_tx = listen_for_enable_presale()
    signed_presale_tx = create_presale_transaction()
    send_bundle(signed_enable_tx, signed_presale_tx)

if __name__ == "__main__":
    main()
