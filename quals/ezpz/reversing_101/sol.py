from pwn import *

key = 0xc1de1494171d9e2f

encrypted_hex = "d158158aeeb5bb520c6ba4ab6d7db7"
encrypted = bytes([int(encrypted_hex[i:i+2], 16) for i in range(0, len(encrypted_hex), 2)])

def rc4_decrypt(data: bytes, key: int) -> bytes:
    key_bytes = key.to_bytes(8, 'little')
    S = list(range(256))

    # Key scheduling
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % 8]) % 256
        S[i], S[j] = S[j], S[i]

    # Pseudo-random generation and decryption
    i = j = 0
    out = bytearray()
    for byte in data:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        out.append(byte ^ K)

    return bytes(out)

plaintext = rc4_decrypt(encrypted, key)
print(plaintext)

answers = ["0x402db6", "strlen", "15", "0xc1de1494171d9e2f", "RC4", "honk-mimimimimi"]

remote = connect("challs.nusgreyhats.org", 33000)

for ans in answers:
    remote.sendline(ans.encode())

remote.recvuntil(b"grey")
print("grey" + remote.recvline().decode())
