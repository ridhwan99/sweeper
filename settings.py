import time
import requests
from decouple import config
from termcolor import cprint
from web3 import Web3
from abi import hexAbi


class MyAccount:

    """
    BLUEPRINT OF ETH ACCOUNT TO  BE MANAGED BY SCRIPT
    """
    ethContractAddress = "0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"
    hexContractAddress = "0x2b591e99afE9f32eAA6214f7B7629768c40Eeb39"

    def __init__(self, ethWalletAddress, walletBAddress, chain='eth'):
        self.privateKey = config(f'{ethWalletAddress}')
        self.ethWalletAddress = ethWalletAddress
        self.walletBAddress = walletBAddress
        if chain == 'eth':
            self.chain = config('INFURA_KEY')
        elif chain == 'pulsechain':
            self.chain = config('pulsechain')

    def createConnection(self):
        """
        CREATES CONNECTION TO ETH MAINNET VIA INFURA API
        :return: <Web3>
        """
        w3 = Web3(Web3.HTTPProvider(self.chain))
        if w3.isConnected() :
            return w3
        else:
            raise Exception("Connection to web3 is unsuccessful")

    def getWalletBalance(self):
        """
        GET ACCOUNT BALANCE OF ETH WALLET
        :return: <float>
        """
        w3 = self.createConnection()
        balance = w3.eth.getBalance(w3.toChecksumAddress(self.ethWalletAddress))
        balance = w3.fromWei(balance, 'ether')
        return balance

    def signTransaction(self, transaction):
        """
        SIGN TRANSACTION AND BROADCAST TO ETH MAINNET
        :param transaction: <dict> transaction to be signed
        :return: void
        """
        w3 = self.createConnection()
        cprint("[+] Signing transaction", "yellow")
        try:
            signed = w3.eth.account.signTransaction(transaction, self.privateKey)
        except TypeError:
            cprint("[+] Invalid key for address \n[+] Signing transaction failed ", "red")
            tx = None

        else:
            cprint("[+] Signing transaction successful", "green")
            cprint("[+] Broadcasting signed transaction", "yellow")
            try:
                tx = w3.eth.sendRawTransaction(signed.rawTransaction)
            except Exception as e:
                print(e)
                cprint("[+] Broadcasting signed transaction failed", "red")
                tx = None
            else:
                cprint("[+] Broadcasting signed transaction successful \n Transaction Hash : " + str(tx.hex()), "green")
                time.sleep(60)
            return tx

    def getHexBalance(self):
        """
        GET BALANCE OF DAI ADDRESS ASSOCIATED WITH ETH ACCOUNT
        :return:<float> or None
        """
        w3 = self.createConnection()
        contract_instance = w3.eth.contract(address=Web3.toChecksumAddress(self.hexContractAddress), abi=hexAbi)
        balance = contract_instance.functions.balanceOf(Web3.toChecksumAddress(self.ethWalletAddress)).call()
        return balance

    def get_fast_gas_price(self):
        response = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
        gas_price = response.json()['fastest'] / 10
        return gas_price

    def send_max_eth(self, recipient_wallet):
        w3 = self.createConnection()
        b = self.getWalletBalance()
        gas_price = self.get_fast_gas_price()
        balance = w3.toWei(b, 'ether')
        gwei = w3.toWei(gas_price, 'gwei')
        b = w3.fromWei(balance, 'ether')
        g = w3.fromWei(gwei*21000, 'ether')
        print(f'{b} eth found')
        print(b, g)
        if balance > gwei * 21000:
            max_send = b - g
            print(max_send, g)
            transaction = {"to": Web3.toChecksumAddress(recipient_wallet),
                           'chainId': 941,
                           "value":  w3.toWei(max_send, 'ether'),
                           "gas": 21000,
                           "gasPrice": gwei,
                           "nonce": w3.eth.getTransactionCount(self.ethWalletAddress)}
            print(transaction)

            return self.signTransaction(transaction)
        else:
            print("not enough gas")

    def send_hex(self, recipient_wallet):
        w3 = self.createConnection()
        hexbalance = self.getHexBalance()
        ebalance = self.getWalletBalance()
        ethbalance = w3.toWei(ebalance, 'gwei')
        nonce = w3.eth.getTransactionCount(self.ethWalletAddress)
        gas_price = self.get_fast_gas_price()
        print(f'Found {hexbalance} hex')
        print(f'{ebalance} eth found for gas')
        if ethbalance > gas_price * 80000 and hexbalance > 1:
            contract_instance = w3.eth.contract(address=Web3.toChecksumAddress(self.hexContractAddress), abi=hexAbi)
            txn = contract_instance.functions.transfer(Web3.toChecksumAddress(recipient_wallet), hexbalance).buildTransaction({'chainId': 1,
                                                                                                                               'gas': 80000,
                                                                                                                               'maxFeePerGas': w3.toWei(gas_price, 'gwei'),
                                                                                                                               'maxPriorityFeePerGas': w3.toWei(gas_price, 'gwei'),
                                                                                                                               'nonce': nonce, })
            return self.signTransaction(txn)
        else:
            print('not enough eth or hex')


