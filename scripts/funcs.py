from brownie import network, accounts, config, MockV3Aggregator, Contract, VRFCoordinatorMock, MockOracle, LinkToken, interface

DEV_ENVS = ["development"]
contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
    "mock_oracle": MockOracle
}

def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in DEV_ENVS:
        if len(contract_type) <= 0:
            deploy_mocks()
        contract = contract_type[-1]
        # MockV3Aggregator[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        contract = Contract.from_abi(
            contract_type._name, contract_address, contract_type.abi
        )
        # MockV3Aggregator.abi
    return contract

DECIMALS = 8
INITIAL_VALUE = 200000000000

def deploy_mocks(decimals=DECIMALS, initial_value=INITIAL_VALUE):
    account = get_account()
    MockV3Aggregator.deploy(decimals, initial_value, {"from": account})
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Deployed Mocks!")

    
def get_account(index=None, _id=None):
    if index:
        return accounts[index]

    if _id:
        return accounts.load(_id)

    if network.show_active() in DEV_ENVS:
        return accounts[0]

    return accounts.add(config["wallets"]["from_key"])

def fund_with_link(contract_address, account=None, link_token=None, amount=100000000000000000):
    account = account if account else get_account()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    # link_token_contract = interface.LinkTokenInterface(link_token.address)
    # tx = link_token_contract.transfer(contract_address, amount, {"From": account})
    tx.wait(1)

    print("--Funded the contract--")
    return tx
