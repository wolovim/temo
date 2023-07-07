from __future__ import annotations
import os
import asyncio
from rich.markdown import Markdown
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, Input, Label, Button
from web3 import AsyncWeb3, AsyncHTTPProvider
from textual import log


class Temo(App):
    """Ethereum wallet in your terminal."""

    CSS_PATH = "temo.css"
    w3 = AsyncWeb3(AsyncHTTPProvider("http://localhost:8555"))

    current_block = reactive("fetching...")
    total_supply_erc20 = reactive("fetching...")
    total_supply_erc721 = reactive("fetching...")

    def __init__(self, deploy_data):
        self.nft_contract = deploy_data["nft_contract"]
        self.token_contract = deploy_data["token_contract"]
        self.account = deploy_data["account"]
        self.provider = deploy_data["provider"]
        super().__init__()

    def compose(self) -> ComposeResult:
        yield Container(
            Static(Markdown("#### Current block:")),
            Static("Fetching current block...", id="cblk"),
            classes="box",
        )

        yield Container(
            Static(Markdown("#### Account lookup:")),
            Horizontal(
                Input(placeholder="Search for an account", id="search-input"),
                Button("Search", variant="primary", id="search"),
                id="search-ui",
            ),
            Static(id="account-results"),
            classes="box",
        )

        # erc20 contract:
        yield Container(
            Static(Markdown("#### Contract")),
            Label(f"Name: {self.token_contract.name()}"),
            Static("Fetching total supply...", id="tsupply-erc20"),
            Button(
                "Mint Tokens!",
                variant="primary",
                id="mint-erc20",
                classes="btn-contract",
            ),
            classes="box",
        )

        # erc721 contract:
        yield Container(
            Static(Markdown("#### Contract")),
            Label(f"Name: {self.nft_contract.name()}"),
            Static("Fetching total supply...", id="tsupply-erc721"),
            Button(
                "Mint NFT!", variant="primary", id="mint-erc721", classes="btn-contract"
            ),
            classes="box",
        )

    async def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        ipt = self.query_one(Input)
        ipt.value = self.account.address
        ipt.focus()
        asyncio.create_task(self.lookup_account(self.account.address))
        self.set_interval(4, self.update_current_block)
        self.set_interval(4, self.update_total_supply_erc20)
        self.set_interval(4, self.update_total_supply_erc721)

    def update_current_block(self) -> None:
        """Method to update the current block."""
        self.current_block = self.provider.get_block("latest").number

    def watch_current_block(self, current_block: float) -> None:
        """Called when the current_block attribute changes."""
        self.query_one("#cblk").update(f"Number: {current_block}")

    # ERC20 reactive
    def update_total_supply_erc20(self) -> None:
        self.total_supply_erc20 = self.token_contract.totalSupply()

    def watch_total_supply_erc20(self, count: int) -> None:
        self.query_one("#tsupply-erc20").update(f"Token supply: {count}")

    def on_total_supply_erc20_changed(self, count) -> None:
        self.query_one("#tsupply-erc20").update(f"Total supply: {count}")

    # ERC721 reactive
    def update_total_supply_erc721(self) -> None:
        self.total_supply_erc721 = self.nft_contract.totalSupply()

    def on_total_supply_erc721_changed(self, count) -> None:
        self.query_one("#tsupply-erc721", Static).update(f"Total supply: {count}")

    def watch_total_supply_erc721(self, count: int) -> None:
        self.query_one("#tsupply-erc721").update(f"Token supply: {count}")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            asyncio.create_task(self.lookup_account(self.query_one(Input).value))
        elif event.button.id == "mint-erc20":
            self.token_contract.mint(
                self.account.address, 1000, sender=self.account, max_fee="100 gwei"
            )
        elif event.button.id == "mint-erc721":
            self.nft_contract.safeMint(
                self.account.address,
                "https://localhost:3001/example",
                sender=self.account,
                max_fee="100 gwei",
            )
        else:
            self.exit()

    async def lookup_account(self, address: str) -> None:
        """Looks up an address."""
        result = {}
        w3 = self.w3
        try:
            # ensure checksummed address
            address = w3.to_checksum_address(address)
            ipt = self.query_one(Input)
            ipt.value = str(address)

            # get balance
            balance = await w3.eth.get_balance(address)
            result["bal"] = w3.from_wei(balance, "ether")

            #  get nonce
            nonce = await w3.eth.get_transaction_count(address)
            result["tx_count"] = nonce

            # erc20 balance
            token_count = self.token_contract.balanceOf(address)
            result["token_count"] = token_count

            # erc721 balance
            nft_count = self.nft_contract.balanceOf(address)
            result["nft_count"] = nft_count

            markdown = self.make_account_markdown(result)
            self.query_one("#account-results", Static).update(Markdown(markdown))
        except:
            self.query_one("#account-results", Static).update(
                Markdown("- (No results)")
            )

    def make_account_markdown(self, results: object) -> str:
        """Convert the results in to markdown."""
        lines = []
        lines.append(f"- balance: {results['bal']} ether")
        lines.append(f"- tx count: {results['tx_count']}")
        lines.append(f"- token count: {results['token_count']}")
        lines.append(f"- nft count: {results['nft_count']}")
        return "\n".join(lines)
