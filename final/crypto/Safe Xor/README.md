# Safe Xor

## Challenge (216 points, 15 solves)

> I added type-checking to xor, so my LFSR should be super secure now!
>
> Author: ariana

## Summary

The challenge presents a custom "Safe Xor" operation, which is used in a Linear Feedback Shift Register (LFSR)-like construction. The twist is that the xor operation is replaced with a 3-valued logic (True, False, None). The goal is to recover the flag from the final state of the LFSR after $2^{999}$ iterations.

## Analysis

The Safe Xor operation can be summarized with the following truth table:

| a     | b     | safeXor(a, b) |
|-------|-------|----------------|
| None  | None  | None           |
| None  | False | False          |
| None  | True  | True           |
| False | None  | False          |
| False | False | True           |
| False | True  | None           |
| True  | None  | True           |
| True  | False | None           |
| True  | True  | False          |

<!-- This operation can be mapped to arithmetic in GF(3), where None = 0, False = 1, True = 2, and the operation is essentially subtraction modulo 3. The LFSR state update can thus be modeled as a linear transformation over GF(3). -->

<!-- Write in a friendlier tone -->

A keen eye will notice that this operation can be mapped to modulo 3 arithmetic, where:

- None = 0
- False = 1
- True = 2

The LFSR state update can thus be modeled as a linear transformation over finite field GF(3). And linear transformations can be represented using matrices, which allows us to leverage exponentiation by squaring to quickly compute the state after a large number of iterations in logarithmic time instead of iterating through each step in linear time.

## Approach

1. Convert the final state (given as a list of True/False/None) to GF(3) values.
2. The LFSR update is a linear operation, so we can represent it as a companion matrix over GF(3). By inverting this matrix and raising it to the appropriate power, we can reverse the LFSR to recover the initial state.
3. The initial state, when mapped back from GF(3) to bits (with a specific mapping), gives the flag in binary. Packing these bits into bytes yields the flag.
4. The full solution is implemented in a SageMath script `solve.sage`.

## Flag

`grey{!safe,_!xor,_wow..,..,.,}`
