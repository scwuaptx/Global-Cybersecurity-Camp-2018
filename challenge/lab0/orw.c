#include <unistd.h>
#include <stdio.h>
#include "mysandbox.h"

char shellcode[200];

int main(){
	setvbuf(stdout,0,2,0);
	printf("Give me your shellcode:");
	read(0,shellcode,200);
	if(strstr(shellcode,"flag")){
		puts("So sad");
		exit(0);
	}
	orw_seccomp(); //only allow open/read/write/exit 
	(*(void(*)())shellcode)();
}
