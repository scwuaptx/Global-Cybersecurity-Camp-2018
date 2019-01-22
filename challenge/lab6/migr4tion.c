#include <stdio.h>

int count = 1337 ;

void read_input(char *buf,unsigned int size){
    int ret ;
    ret = read(0,buf,size);
    if(ret <= 0){
        puts("read error");
        _exit(1);
    }
    if(buf[ret-1] == '\n')
        buf[ret-1] = '\x00';
}
int main(){
	if(count != 1337)
		_exit(1);
	count++;
	char buf[48];
	setvbuf(stdout,0,2,0);
	setvbuf(stdin,0,2,0);
	puts("Try your best :");
	read_input(buf,128);
	return ;	
}
