// SPDX-License-Identifier: MIT
pragma solidity ^0.6.6;

interface ILendingPoolAddressesProvider {
    function getLendingPool() external view returns(address);
}