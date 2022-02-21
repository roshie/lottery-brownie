from brownie import network, Lottery, config
from scripts.funcs import get_account, get_contract, fund_with_link
import time

def deploy_lottery():
    # The default account the owner of this lottery
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyHash"],
        {
           "from": account
        })
    print("Deployed Lottery 🎉🎉")
    return lottery

def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    start_lottery = lottery.startLottery({"from": account})
    start_lottery.wait(1)

    print("Lottery Started")

def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 10000000
    enter_tx = lottery.enter({"from": account, "value": value})
    enter_tx.wait(1)

    print("You Entered the Lottery !!!")

def end_lottery():
    account = get_account()
    lottery = Lottery[-1]

    # fund the contract and end the lottery
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    end_tx = lottery.endLottery({"from": account})
    end_tx.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the Winner")

def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

