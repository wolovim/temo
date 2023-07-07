# Temo

Temo == (Ethereum) Textual Demo

This is a little hackathon helper repo to show how to display some basic Ethereum functionality in a terminal UI.

<img width="585" alt="temo-screenshot" src="https://github.com/wolovim/temo/assets/3621728/32ee2aa8-2351-4e65-9135-3a055e4c46b6">

Tools used:

-   [Ape](https://snakecharmers.ethereum.org/intro-to-ape/): smart contract development framework used to compile and deploy contracts, and run scripts
-   [Anvil](https://book.getfoundry.sh/anvil/) ([Foundry](https://book.getfoundry.sh/)): a local test network
-   [Textual](https://textual.textualize.io/): Python library for building a user interface in the terminal

# Quickstart

-   Clone this repo, cd into the directory, and create a new virtualenv
-   [Install Foundry](https://book.getfoundry.sh/getting-started/installation)
-   `pip install eth-ape textual`
-   `ape plugins install .`
-   `ape compile`
-   `ape run ui --network ::foundry`
    -   Troubleshooting: on Mac, may need to `brew install libusb`
