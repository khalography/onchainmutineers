// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title BootyToken
 * @dev The native ERC20 token ($BOOTY) for the Onchain Mutineers project.
 * Implements a dynamic "Storm Tax" on selling into Automated Market Maker (AMM) pairs.
 */
contract BootyToken is ERC20, Ownable {
    
    // The current Storm Tax rate in basis points (e.g. 500 = 5%)
    uint256 public taxRateBps = 500;
    
    // Address of the treasury/vault that collects taxes
    address public vaultAddress;
    
    // AMM pool addresses where trades are tax-levied (e.g., Uniswap LP pools)
    mapping(address => bool) public ammPairs;
    
    // Exclude specific addresses from paying taxes (e.g., the owner, the vault, routing contracts)
    mapping(address => bool) public isExcludedFromFees;

    event StormTaxUpdated(uint256 indexed oldTaxBps, uint256 indexed newTaxBps);
    event VaultAddressUpdated(address indexed oldVault, address indexed newVault);
    event AMMPairStatusUpdated(address indexed pair, bool indexed isAMM);
    event ExcludeFromFeesUpdated(address indexed account, bool indexed isExcluded);

    constructor(address _initialVault) 
        ERC20("BootyToken", "BOOTY") 
        Ownable(msg.sender) 
    {
        require(_initialVault != address(0), "Vault cannot be zero address");
        vaultAddress = _initialVault;
        
        isExcludedFromFees[msg.sender] = true;
        isExcludedFromFees[_initialVault] = true;
        isExcludedFromFees[address(this)] = true;

        // Pre-mint a fixed supply for initial liquidity and reserves (e.g. 100,000,000 $BOOTY)
        _mint(msg.sender, 100_000_000 * 10**decimals());
    }

    /**
     * @notice Updates the tax rate representing market volatility (Dynamic Storm Tax).
     * @dev Taxes are capped between 2% (200 bps) and 8% (800 bps) to prevent excessive taxation.
     * @param _newTaxBps New tax rate in basis points.
     */
    function setStormTax(uint256 _newTaxBps) external onlyOwner {
        require(_newTaxBps >= 200 && _newTaxBps <= 800, "Tax rate must be between 2% and 8%");
        uint256 oldTax = taxRateBps;
        taxRateBps = _newTaxBps;
        emit StormTaxUpdated(oldTax, _newTaxBps);
    }

    /**
     * @notice Sets the target address for fees collected.
     */
    function setVaultAddress(address _newVault) external onlyOwner {
        require(_newVault != address(0), "Vault cannot be zero address");
        address oldVault = vaultAddress;
        vaultAddress = _newVault;
        isExcludedFromFees[_newVault] = true;
        emit VaultAddressUpdated(oldVault, _newVault);
    }

    /**
     * @notice Registers or removes an address as an AMM pair (LP Pool).
     */
    function setAMMPair(address _pair, bool _isAMM) external onlyOwner {
        ammPairs[_pair] = _isAMM;
        emit AMMPairStatusUpdated(_pair, _isAMM);
    }

    /**
     * @notice Excludes or includes an account from fee taxes.
     */
    function setExcludedFromFees(address _account, bool _isExcluded) external onlyOwner {
        isExcludedFromFees[_account] = _isExcluded;
        emit ExcludeFromFeesUpdated(_account, _isExcluded);
    }

    /**
     * @dev Overridden ERC20 transfer hook that applies tax fees on sells to AMM pairs.
     */
    function _update(
        address from,
        address to,
        uint256 value
    ) internal override {
        // Exclude mint, burn, and excluded address transfers from fees
        if (from == address(0) || to == address(0) || isExcludedFromFees[from] || isExcludedFromFees[to]) {
            super._update(from, to, value);
            return;
        }

        uint256 taxAmount = 0;

        // Apply tax on SELLS (transfers going into an AMM LP Pool)
        if (ammPairs[to]) {
            taxAmount = (value * taxRateBps) / 10000;
        }

        if (taxAmount > 0) {
            super._update(from, vaultAddress, taxAmount);
            super._update(from, to, value - taxAmount);
        } else {
            super._update(from, to, value);
        }
    }
}
