# Temo

Temo == (Ethereum) Textual Demo

This is a little hackathon helper repo to show how to display some basic Ethereum functionality in a terminal UI.

Tools used:

-   [Ape](https://snakecharmers.ethereum.org/intro-to-ape/): smart contract development framework used to compile and deploy contracts, and run scripts
-   [Anvil](https://book.getfoundry.sh/anvil/) ([Foundry](https://book.getfoundry.sh/)): a local test network
-   [Textual](https://textual.textualize.io/): Python library for building a user interface in the terminal

# Quickstart

-   Clone this repo, cd into the directory, and create a new virtualenv
-   `pip install eth-ape textual`
-   `ape plugins install .`
-   `ape compile`
-   `ape run ui --network ::foundry`
    -   Troubleshooting: on Mac, may need to `brew install libusb`
