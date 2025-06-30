# Locker

## Challenge (964 points, 4 solves)

> I don't trust myself to hold my funds, so I wrote a contract to lock them until next year. There's no way I lose them now, right...?
>
> `nc challs3.nusgreyhats.org 34221`
>
> Author: MiloTruck

## Summary

A smart contract challenge involving a vault that can lock both ERC20 tokens and ERC721 NFTs, but with a subtle bug in how it distinguishes between the two.

Readings for ERC20 and ERC721:

- [ERC20 Fungible Token Standard](https://docs.openzeppelin.com/contracts/5.x/erc20)
- [ERC721 Non-Fungible Token Standard](https://docs.openzeppelin.com/contracts/5.x/erc721)

## Analysis

The contract exposes two functions: `lockToken` and `lockNFT`. However, neither function checks if the asset being locked is actually a token or an NFT. This opens up the possibility of passing an NFT to the token function, or vice versa, leading to confusion in the contract's internal accounting.

## Approach

By passing an NFT with id 1338 to lockToken and then withdrawing it with unlockToken using the id 1337, we can trick the contract into releasing an NFT we do not own. This works because the contract treats tokens as fungible and does not properly check ownership for NFTs in the token logic.

## Flag

`grey{token_confusion_64c46db}`
