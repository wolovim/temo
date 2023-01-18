from __future__ import annotations
import os
import asyncio
from rich.markdown import Markdown
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widget import Widget
from textual.widgets import Static, Input, Label, Button
from web3 import Web3, AsyncHTTPProvider
from web3.eth import AsyncEth


class CurrentBlock(Static):
    """A widget to display the current block."""

    current_block = reactive("fetching...")

    def __init__(self, provider):
        self.provider = provider
        super().__init__()

    def on_mount(self) -> None:
        """Event handler called when widget is added to the app."""
        self.set_interval(3, self.update_current_block)

    def update_current_block(self) -> None:
        """Method to update the current block."""
        self.current_block = self.provider.get_block("latest").number

    def watch_current_block(self, current_block: float) -> None:
        """Called when the current_block attribute changes."""
        self.update(f"Current block: {current_block}")


#  class ContractContainer(Static):
    #  """A widget to displays contract methods and state."""

    #  def __init__(self, contract, account):
        #  self.contract = contract
        #  self.account = account
        #  super().__init__()

    #  def compose(self) -> ComposeResult:
        #  yield Label(f"X Name: {self.contract.name()}"),
        #  yield Label(f"Total supply: {self.contract.totalSupply()}"),
        #  yield Button("Mint!", variant="primary"),
        #  # self.token_contract.mint(account.address, 1000, sender=account)

    #  def on_button_pressed(self, event: Button.Pressed) -> None:
        #  self.contract.mint(self.account.address, 1000, sender=self.account)


class Temo(App):
    """Ethereum wallet in your terminal."""

    CSS_PATH = "temo.css"
    w3 = Web3(
        AsyncHTTPProvider('http://localhost:8545'),
        modules={"eth": (AsyncEth,)},
        middlewares=[]
    )

    current_block = reactive("fetching...")
    total_supply = reactive("fetching...")

    def __init__(self, contracts):
        self.nft_contract = contracts["nft_contract"]
        self.token_contract = contracts["token_contract"]
        self.account = contracts["account"]
        self.provider = contracts["provider"]
        super().__init__()

    def compose(self) -> ComposeResult:
        #  yield CurrentBlock(self.provider)
        yield Container(
            Static(Markdown("#### Current block:")),
            Static("loading...", id="cblk"),
            classes="box"
        )

        yield Container(
            Static(Markdown("#### Account lookup:")),
            Horizontal(
                Input(placeholder="Search for an account", id="search-input"),
                Button("Search", variant="primary", id="search"),
                id="search-ui"
            ),
            Static(id="results"),
            classes="box"
        )

        # token contract:
        yield Container(
            Static(Markdown("#### Contract")),
            Label(f"Name: {self.token_contract.name()}"),
            Static("Loading total supply...", id="tsupply"),
            Button("Mint!", variant="primary"),
            classes="box"
        )

        # nft contract:
        yield Container(
            Static(Markdown("#### Contract")),
            Label(f"Name: {self.nft_contract.name()}"),
            classes="box"
        )
    
    async def on_mount(self) -> None:
        """Called when app starts."""
        # Give the input focus, so we can start typing straight away
        ipt = self.query_one(Input)
        ipt.value = self.account.address
        ipt.focus()
        asyncio.create_task(self.lookup_account(self.account.address))
        self.set_interval(3, self.update_current_block)
        self.set_interval(3, self.update_total_supply)

    def update_current_block(self) -> None:
        """Method to update the current block."""
        self.current_block = self.provider.get_block("latest").number

    def watch_current_block(self, current_block: float) -> None:
        """Called when the current_block attribute changes."""
        self.query_one("#cblk").update(f"Number: {current_block}")
        self.update_total_supply()

    def update_total_supply(self) -> None:
        self.total_supply = self.token_contract.totalSupply()

    def watch_total_supply(self, supply: int) -> None:
        self.query_one("#tsupply").update(f"Token supply: {supply}")

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            pass
            # lookup
        else:
            self.token_contract.mint(self.account.address, 1000, sender=self.account)

    def on_total_supply_changed(self, total_supply) -> None:
        self.query_one("#tsupply", Static).update(f"Total supply: {total_supply}")

    # TODO: change to search button based lookup
    async def on_input_changed(self, message: Input.Changed) -> None:
        """A coroutine to handle a text changed message."""
        if message.value:
            # Look up the account in the background
            asyncio.create_task(self.lookup_account(message.value))
        else:
            # Clear the results
            self.query_one("#results", Static).update()

    async def lookup_account(self, account: str) -> None:
        """Looks up an account."""
        result = {}

        # get balance
        result["bal"] = self.w3.from_wei(self.account.balance, 'ether')

        # get tx count
        result["tx_count"] = self.account.nonce

        if account == self.query_one(Input).value:
            markdown = self.make_account_markdown(result)
            self.query_one("#results", Static).update(Markdown(markdown))

    def make_account_markdown(self, results: object) -> str:
        """Convert the results in to markdown."""
        lines = []
        lines.append(f"- balance: {results['bal']} ether")
        lines.append(f"- tx count: {results['tx_count']}")

        return "\n".join(lines)


if __name__ == "__main__":
    app = Temo()
    app.run()
