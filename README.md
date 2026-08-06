# Onchain Mutineers 🏴‍☠️⚡

**Onchain Mutineers** is a gamified, community-driven NFT project built on the Robinhood Chain (Arbitrum Orbit L2). Inspired by classic pirate lore with a high-contrast cyberpunk aesthetic, it features active economic game loops designed to align incentives between creators, collectors, and token traders.

---

## 🚀 The Core Mechanics

1. **The Crew (NFTs):** 1,111 Onchain Mutineers. Minted via a public OpenSea Drop.
2. **The Booty ($BOOTY):** The native ERC-20 utility token.
3. **Dynamic Storm Taxes:** Sells of `$BOOTY` are taxed dynamically based on market volatility (representing "smooth sailing" or "rough storms" on the digital seas). Taxes range from 2% (low volatility) to 8% (high volatility) and are sent directly to the **Plunder Vault**.
4. **The Saturday Mutiny (Weekly Vote):** Every Saturday, the vault opens. NFT holders vote off-chain (e.g., via Snapshot.org) on how to allocate the accumulated loot:
   - **Plunder the Captain:** Distribute 60% of the vault to NFT holders (with **smallest wallets receiving a "scurvy bonus" weight** to encourage distribution).
   - **Bury the Treasure:** Use 60% of the vault to buy back `$BOOTY` from the open market and burn it, raising token scarcity.
   - The remaining 40% of the vault goes to marketing/operations and a special reward pool for the rare "First Mates" and "Captains" (Legendary NFTs).
5. **Walk the Plank (Streak Reset):** To prevent paper-hands, holding your Onchain Mutineer NFT increases your "Cabin Crew Streak" (up to 2x yield/voting weight after 10 weeks). If you transfer or sell **any** of your Onchain Mutineers NFTs, your streak resets to zero. This is tracked off-chain via blockchain event indexing.

---

## 📁 Directory Structure

```text
onchainmutineers/
├── README.md                  # Project overview and specifications
├── contracts/                 # Smart contracts (Solidity)
│   ├── BootyToken.sol         # ERC-20 token with dynamic fees
│   └── PlunderVault.sol       # Treasury contract managing Saturday Mutiny distributions
└── scripts/                   # Tooling and generator scripts
    └── art_generator.py       # Programmatic layered art generator
```

---

## 🛠️ Getting Started

1. **Set this folder as your active workspace:** Open the `onchainmutineers` directory in your IDE.
2. **Populate Traits:** Place your transparent PNG layers into `scripts/traits/` folders.
3. **Generate Art:** Run `python scripts/art_generator.py` to compile the 1,111 assets and metadata.
4. **Compile & Deploy Contracts:** Use Hardhat or Foundry to deploy `BootyToken.sol` and `PlunderVault.sol` onto the Robinhood Chain.

