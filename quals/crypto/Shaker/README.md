# Shaker

## Challenge (705 points, 87 solves)

> You found a shaker. Can you get the flag out?
>
> nc challs.nusgreyhats.org 33302
>
> Author: hadnot

## Summary

The challenge provides a "shaker" encryption service. Initially, there is a random key and permutation of length 64. There are two operations that we can perform:

1. **Shake the shaker**: XOR the flag with the key, then permute it using the current permutation.
2. **See inside**: print a snapshot of the current flag XOR with the key, then the service generates a new permutation and does **Shake the shaker** by itself.

## Analysis

Let the original flag be $F$, the fixed key be $x$, and the current permutation be $P_i$. The "See inside" option provides an output $Y = S_i \oplus x$, where $S_i$ is the current state ($S_0 = F$ initially). After revealing the output, the state is updated to $S_{i+1} = P_{i+1}(Y \oplus x) = P_{i+1}(S_i)$.

This means the internal state $S_i$ is always a permutation of the original flag $F$. Therefore, every output $Y_i$ we receive is always a random permutation of the flag XORed with the key.

The critical vulnerability is that the key $x$ is constant across all operations. This is analogous to a many-time pad, but with a permuted plaintext. Since the flag alphabet is contrained to a whitelist: `abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_{}`, we can determine each byte of the key $x[i]$ by finding a value that, when XORed with all collected output bytes for that position, consistently results in a printable character.

## Approach

The solution is a statistical attack to recover the key $x$.

1. Connect to the server and repeatedly call the "See inside" option (~200 times) to gather a list of outputs $Y_0, Y_1, \ldots$.
2. For each byte position $i$ from 0 to 63, find the unique key byte $x[i]$ such that $Y_0[i] \oplus x[i], Y_1[i] \oplus x[i], \ldots$ are all characters in the whitelist.
3. Once the key $x$ is uniquely determined, compute the flag using the first output: $F = Y_0 \oplus x$.

## Flag

`grey{kinda_long_flag_but_whatever_65k2n427c61ww064ac3vhzigae2qg}`
