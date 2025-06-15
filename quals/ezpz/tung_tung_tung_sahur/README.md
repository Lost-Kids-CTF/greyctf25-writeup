# Tung Tung Tung Sahur

## Challenge (100 points, 414 solves)

> New to the world of brainrot? Not sure what names to pick from? We've got you covered with a list of our faves:
>
> - Tralalero Tralala
> - Chef Crabracadabra
> - Boneca Ambalabu
> - Tung Tung Tung Tung Tung Tung Tung Tung Tung Sahur
>
> Author: elijah5399

## Summary

Decrypte RSA to get the flag.

## Analysis

The challenge uses RSA encryption with a small public exponent `e = 3`. From [Wikipedia](https://en.wikipedia.org/wiki/RSA_cryptosystem#:~:text=Attacks%20against%20plain%20RSA,-There%20are%20a&text=When%20encrypting%20with%20low%20encryption,the%20ciphertext%20over%20the%20integers.):

> When encrypting with low encryption exponents (e.g., $e = 3$) and small values of the $m$ (i.e., $m < n^{1/e}$), the result of $m^e$ is strictly less than the modulus $n$. In this case, ciphertexts can be decrypted easily by taking the $e$-th root of the ciphertext over the integers.

## Approach

Recover the original value of `C` by reading the number of lines in `output.txt` and reverse the logic. Use `nth_root` from `sagemath` to compute the cube root of the ciphertext.

## Flag

`grey{tUn9_t00nG_t0ONg_x7_th3n_s4hUr}`
