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

    deployed_erc20 = account.deploy(project.FungibleDemo, max_fee="100 gwei")
    deployed_erc721 = account.deploy(project.NftDemo, max_fee="100 gwei")

    deploy_data = {
        'account': account,
        'provider': networks.active_provider,
        'nft_contract': deployed_erc721,
        'token_contract': deployed_erc20,
    }

    Temo(deploy_data=deploy_data).run()
