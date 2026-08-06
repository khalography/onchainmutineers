// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/IERC20.sol";
import "@openzeppelin/contracts/access/Ownable.sol";

/**
 * @title PlunderVault
 * @dev Simple treasury and distributor contract that holds collected taxes ($BOOTY)
 * and allows the owner or authorized distributors to batch transfer tokens to winners
 * of the Saturday Mutiny based on off-chain streak and distribution calculations.
 */
contract PlunderVault is Ownable {

    IERC20 public bootyToken;

    // Authorized distributor addresses (e.g. backend script/bot)
    mapping(address => bool) public isDistributor;

    event TokensDistributed(address indexed distributor, uint256 totalAmount, uint256 recipientCount);
    event DistributorStatusUpdated(address indexed distributor, bool indexed isAuthorized);
    event BootyTokenAddressUpdated(address indexed oldToken, address indexed newToken);

    modifier onlyDistributorOrOwner() {
        require(msg.sender == owner() || isDistributor[msg.sender], "Not authorized distributor or owner");
        _;
    }

    constructor() Ownable(msg.sender) {}

    /**
     * @notice Set the ERC20 token address ($BOOTY).
     */
    function setBootyToken(address _bootyToken) external onlyOwner {
        require(_bootyToken != address(0), "Token cannot be zero address");
        address oldToken = address(bootyToken);
        bootyToken = IERC20(_bootyToken);
        emit BootyTokenAddressUpdated(oldToken, _bootyToken);
    }

    /**
     * @notice Set or revoke distributor authorization.
     */
    function setDistributor(address distributor, bool authorized) external onlyOwner {
        require(distributor != address(0), "Distributor cannot be zero address");
        isDistributor[distributor] = authorized;
        emit DistributorStatusUpdated(distributor, authorized);
    }

    /**
     * @notice Batch transfers $BOOTY to recipients based on off-chain Saturday Mutiny calculations.
     * @param recipients Array of recipient addresses.
     * @param amounts Array of token amounts to distribute.
     */
    function batchTransfer(
        address[] calldata recipients, 
        uint256[] calldata amounts
    ) external onlyDistributorOrOwner {
        require(recipients.length == amounts.length, "Array lengths mismatch");
        require(recipients.length > 0, "No recipients provided");
        require(address(bootyToken) != address(0), "Booty token address not set");

        uint256 totalAmount = 0;
        for (uint256 i = 0; i < recipients.length; i++) {
            address recipient = recipients[i];
            uint256 amount = amounts[i];
            require(recipient != address(0), "Cannot transfer to zero address");
            
            totalAmount += amount;
            require(bootyToken.transfer(recipient, amount), "Transfer failed");
        }

        emit TokensDistributed(msg.sender, totalAmount, recipients.length);
    }

    /**
     * @notice Emergency/operational withdrawal of $BOOTY tokens.
     */
    function withdrawBooty(address to, uint256 amount) external onlyOwner {
        require(to != address(0), "Recipient cannot be zero address");
        require(address(bootyToken) != address(0), "Booty token address not set");
        require(bootyToken.transfer(to, amount), "Withdrawal failed");
    }

    /**
     * @notice Emergency withdrawal for any ERC20 token sent to this contract by mistake.
     */
    function withdrawAnyERC20(address token, address to, uint256 amount) external onlyOwner {
        require(token != address(0), "Token cannot be zero address");
        require(to != address(0), "Recipient cannot be zero address");
        require(IERC20(token).transfer(to, amount), "Withdrawal failed");
    }
}
