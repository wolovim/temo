// Important: config generated by ape! If you have a hardhat config already,
// ape won't override it and won't be able to find the test accounts associated.

// See https://hardhat.org/config/ for config options.
module.exports = {
  networks: {
    hardhat: {
      hardfork: "london",
      // Base fee of 0 allows use of 0 gas price when testing
      // initialBaseFeePerGas: 0,
      accounts: {
        mnemonic: "test test test test test test test test test test test junk",
        path: "m/44'/60'/0'",
        count: 10,
      },
      mining: {
        auto: false,
        interval: 5000,
      },
    },
  },
};
