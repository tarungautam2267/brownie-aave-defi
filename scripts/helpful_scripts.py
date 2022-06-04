from brownie import network, config, accounts
LOCAL_BLOCKCHAIN_ENVIRONMENT = ["development", "ganache-local", "mainnet-fork", "mainnet-fork-dev"]
DECIMALS = 8
STARTING_PRICE = 200000000000

def get_account():
    if (network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENT):
        account = accounts[0]
        return account
    else:
        return accounts.add(config["wallets"]["from_key"])