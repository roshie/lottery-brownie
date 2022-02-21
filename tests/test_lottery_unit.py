from brownie import Lottery, accounts, config, network
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest
from scripts.funcs import DEV_ENVS, fund_with_link, get_account, get_contract

def test_get_entrance_fee():
    if network.show_active() not in DEV_ENVS:
        pytest.skip()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()

    assert entrance_fee == Web3.toWei(0.025, "ether")


def test_lottery_winner():
    if network.show_active() not in DEV_ENVS:
        pytest.skip()
    # Arrange
    lottery = deploy_lottery()
    account = get_account()
    entrance_fee = lottery.getEntranceFee()
    STATIC_RNG = 777

    # Act
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entrance_fee})
    lottery.enter({"from": get_account(index=1), "value": entrance_fee})
    lottery.enter({"from": get_account(index=2), "value": entrance_fee})
    fund_with_link(lottery)

    transaction = lottery.endLottery({"from": account})
    request_id = transaction.events["RequestedRandomness"]["requestId"]
    get_contract("vrf_coordinator").callBackWithRandomness(request_id, STATIC_RNG, lottery.address, {"from": account})

    starting_balance = account.balance()
    balance_of_lottery = lottery.balance()
    
    # Assert
    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert account.balance() == starting_balance + balance_of_lottery