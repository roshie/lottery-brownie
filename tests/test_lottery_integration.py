from time import time
from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.funcs import DEV_ENVS, fund_with_link, get_account, get_contract


def test_can_pick_winner():
    if network.show_active() in DEV_ENVS:
        pytest.skip()

    lottery = deploy_lottery()
    account = get_account()
    entrance_fee = lottery.getEntranceFee()

    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entrance_fee})
    lottery.enter({"from": account, "value": entrance_fee})
    lottery.enter({"from": account, "value": entrance_fee})
    fund_with_link(lottery)

    lottery.endLottery({"from": account})
    time.sleep(60)

    assert lottery.recentWinner() == account, lottery.recentWinner()
    assert lottery.balance() == 0