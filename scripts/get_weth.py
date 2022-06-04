from web3 import Web3
from scripts.helpful_scripts import get_account
from brownie import interface, config, network
def get_weth():
    account = get_account()
    weth = interface.WethInterface(config["networks"][network.show_active()]["weth_token"])
    tx = weth.deposit({"from": account, "value": Web3.toWei(0.1,"ether")})
    tx.wait(1)
    print("WETH Received")
    return tx
def withdraw():
    account = get_account()
    weth = interface.WethInterface(config["networks"][network.show_active()]["weth_token"])
    tx = weth.withdraw(Web3.toWei(0.1,"ether"),{"from": account})
    print("ETH Received")
    return tx
def main():
    get_weth()
