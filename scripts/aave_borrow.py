from scripts.helpful_scripts import get_account
from scripts.get_weth import get_weth
from brownie import config, network, interface
from web3 import Web3
amm = 0.1
def main():
    account=get_account()
    erc20_address=config["networks"][network.show_active()]["weth_token"]
    if network.show_active() in ["mainnet-fork"]:
        get_weth()
    lending_pool = get_lending_pool()
    print(lending_pool)
    approve_erc20(Web3.toWei(amm,"ether"), lending_pool.address,erc20_address,account)
    print("Staking...")
    tx = lending_pool.deposit(erc20_address,Web3.toWei(amm,"ether"),account.address,0,{"from":account})
    tx.wait(1)
    print(f"{amm} WETH STAKED!!!")
    borrowable_eth,total_debt =get_borrowable_data(lending_pool, account)
    dai_eth_price = get_asset_price(config["networks"][network.show_active()]["dai_eth_price"])
    amount_dai_to_borrow = (1/dai_eth_price) * (borrowable_eth*0.95)
    print(f"Going to borrow {amount_dai_to_borrow}")
    dai_token = config["networks"][network.show_active()]["dai_token"]
    print("Borrowing...")
    tx = lending_pool.borrow(dai_token, Web3.toWei(amount_dai_to_borrow,"ether"),1,0,account.address,{"from":account})
    tx.wait(1)
    print("Borrowed Dai Successfully!!!")
    borrowable_eth,total_debt= get_borrowable_data(lending_pool, account)
    repay_all(amount_dai_to_borrow, lending_pool, account)
    get_borrowable_data(lending_pool, account)

def repay_all(amount, lending_pool, account):
    print("Repaying Loan...")
    approve_erc20(Web3.toWei(amount, "ether"),lending_pool, config["networks"][network.show_active()]["dai_token"],account)
    tx = lending_pool.repay(config["networks"][network.show_active()]["dai_token"], amount, 1, account.address, {"from":account})
    tx.wait(1)
    print("Loan Repaid!!")

def get_asset_price(price_feed_address):
        dai_eth_price = interface.AggregatorV3Interface(price_feed_address)
        latest_price = dai_eth_price.latestRoundData()[1]
        converted_price = Web3.fromWei(latest_price,"ether")
        print(f"Dai/Eth price is {converted_price}")
        return float(converted_price)


def get_borrowable_data(lending_pool, account):
    (total_collateral, total_debt, available_borrow, current_liquidation_threshold, ltv, healthfactor) = lending_pool.getUserAccountData(account.address)
    total_collateral = Web3.fromWei(total_collateral,"ether")
    print(f"Total collateral {total_collateral}")
    total_debt= Web3.fromWei(total_debt,"ether")
    print(f"Total debt {total_debt}")
    available_borrow= Web3.fromWei(available_borrow,"ether")
    print(f"available to borrow {available_borrow}")
    return(float(available_borrow),float(total_debt))

def approve_erc20(amount, spender, erc20_address, account):
    print("Approving ERC20...")
    erc20 = interface.IERC20(erc20_address)
    tx = erc20.approve(spender, amount, {"from":account})
    tx.wait(1)
    print("WETH Approved!")
    return tx

def get_lending_pool():
    lending_pool_add_pro = interface.ILendingPoolAddressesProvider(config["networks"][network.show_active()]["lending_pool_add"])
    lending_pool_add = lending_pool_add_pro.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_add)
    return lending_pool