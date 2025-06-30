from sage.all import *

# 1) Original boolean/None array (True, False, None)
iv = [True, True, False, True, True, True, None, True, True, False, False, False, None, False, True, True, None, True, True, True, True, False, True, None, False, None, None, None, False, None, False, True, True, True, True, False, False, False, False, False, None, True, True, None, None, False, None, None, False, True, True, False, None, None, None, None, False, False, False, False, False, False, None, None, True, None, True, None, True, False, None, True, False, False, None, None, True, None, True, None, None, True, None, False, None, True, False, True, None, True, None, False, False, False, True, False, False, True, False, False, None, True, False, False, False, True, None, False, True, None, False, None, False, True, True, None, False, True, True, False, None, None, True, True, False, True, None, True, True, True, True, True, False, None, True, None, None, None, None, None, True, None, True, True, True, False, None, False, True, True, True, False, None, True, None, True, True, False, None, None, False, False, False, False, False, None, False, True, None, None, True, True, True, False, False, True, None, None, True, False, True, False, None, True, True, False, False, True, None, True, True, False, None, True, True, True, None, True, True, False, False, True, False, False, None, True, None, False, True, False, False, True, False, False, None, False, True, False, None, None, True, None, True, False, True, None, None, True, None, False, True, True, None, True, False, None, False, False, None]

# 2) Convert to GF(3) encoding: None -> 0, False -> 1, True -> 2
final_state = [0 if x is None else 1 if x is False else 2 for x in iv]

# 3) Build the GF(3) companion matrix of size L×L
F = GF(3)
L = len(final_state)
M = Matrix(F, L, L, lambda i,j: 1 if (i == j-1) else (1 if i == L-1 else 0))

# 4) Invert it, then raise to the 2^999 power
M_inv     = M.inverse()
step_back = M_inv^(2^999)

# 5) Apply to your final state vector
v_final = vector(F, final_state)
v_init  = step_back * v_final

# 6) Convert GF(3) entries back to bits (1→0, 2→1), pack to ASCII
bits = [ (int(v_init[i]) - 1) % 2 for i in range(L) ]

# 7) Prepend a 0 bit to the start
modified_bits = [0] + bits

# 8) Recover the flag from bits
flag = "".join(
    chr(sum(modified_bits[8*k + j] << (7-j) for j in range(8)))
    for k in range((L+1)//8)
)
print("Flag:", flag)
