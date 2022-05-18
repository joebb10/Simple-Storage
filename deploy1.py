from unicodedata import name
from solcx import compile_standard, install_solc
import json
from web3 import Web3
import os
from dotenv import load_dotenv
import web3

load_dotenv()


with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

# Compile Solidity
install_solc("0.6.0")
compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)


# calling the code and putting it on a json file (compiled_code.json)
with open("compiled_code.json", "w") as file:
    json.dump(compiled_sol, file)

# get bytecode

bytecode = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"][
    "bytecode"
]["object"]
# this part the computer will pass for each part inside the contract until it arrive on the "bytecode" and get its object

# get ABI

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


# for connecting to Ganache;
w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
chain_id = 1337
my_address = 0xEABD2ACC3AFC6259EDA3D7503105D4017745EC83
# Colocar "export [o nome da variavel que voce deseja] + o que deseja" e chamar ela com o "os.getenv()"
# import os
# print(os.getenv("SOME_OTHER_VAR"))
private_key = os.getenv("PRIVATE_KEY")


# ganache-cli --deterministic e a parte de deploy, não está funcionando.


# Create the contract in python

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bytecode)
# Get the latest transaction
nonce = w3.eth.getTransactionCount(my_address)
# print(nonce)

# 1- Build a transaction
# 2- Sign a transaction
# 3- Send a transaction

transaction = SimpleStorage.constructor().buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce,
    }
)

sign_txn = w3.eth.account.sign_transaction(transaction, private_key=private_key)

# send this signed transaction
print("Deploying contract...")
tx_hash = w3.eth.send_raw_transaction(sign_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Deployed!")


simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)
# Call --> Simulate making the call and getting a return value
# Transact --> Actually make a state change
print("Updating Contract...")
# Initial value of favorite number
print(simple_storage.functions.retrieve().call())
store_transaction = simple_storage.functions.store(15).buildTransaction(
    {
        "gasPrice": w3.eth.gas_price,
        "chainId": chain_id,
        "from": my_address,
        "nonce": nonce + 1,
    }
)
signed_store_txn = w3.eth.account.sign_transaction(
    store_transaction, private_key=private_key
)
send_store_tx = w3.eth.send_raw_transaction(signed_store_txn.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)
print("Updated!")
print(simple_storage.functions.retrieve().call())

# Não estou conseguindo instalar o "yarn" por algum motivo, e provavelmente é algo como o que aconteceu com o "pip"
# Problema acima resolvido utilizando o "sudo npm install --global yarn" e para chegar a versão: "yarn"
