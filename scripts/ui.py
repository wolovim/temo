from ape import project, accounts, networks
from ape.cli import get_user_selected_account, ape_cli_context
import click
import sys
sys.path.append('../ui')
from ui import Temo

@ape_cli_context()
def main(cli_ctx):
    ecosystem_name = networks.provider.network.ecosystem.name
    network_name = networks.provider.network.name
    provider_name = networks.provider.name
    click.echo(f"You are connected to network '{ecosystem_name}:{network_name}:{provider_name}'.")

    #  account = get_user_selected_account()
    account = cli_ctx.account_manager.test_accounts[0]

    # lol, hardhat workaround to fund ape-native test account
    # TODO: try with hh config deleted
    networks.active_provider.set_balance(account.address, 10000000000000000000000)

    d = account.deploy(project.FungibleDemo)
    e = account.deploy(project.NftDemo)

    # TODO: pass along...
    #   - network?
    #   - w3 instance?
    x = {
        'account': account,
        'provider': networks.active_provider,
        'nft_contract': e,
        'token_contract': d,
    }

    # TODO: grab/display each method off each contract
    #   - off web3 or ape?

    #  import pdb; pdb.set_trace() # noqa
    # ABI? d.contract_type.abi
    Temo(contracts=x).run()
