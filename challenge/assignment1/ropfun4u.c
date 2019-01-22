#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>

#define TIMEOUT 60
void handler(int signum){
    _exit(1);
}

void init_proc(){
    setvbuf(stdin,0,2,0);
    setvbuf(stdout,0,2,0);
    setvbuf(stderr,0,2,0);
    signal(SIGALRM,handler);
    alarm(TIMEOUT);
}
size_t read_input(char *buf,unsigned int size){
    int ret ;
    ret = read(0,buf,size);
    if(ret <= 0){
        _exit(1);
    }
    if(buf[ret-1] == '\n')
        buf[ret-1] = '\x00';
	return ret;
}

int main(){
	char buf[0x20];
	init_proc();
	read_input(buf,0x50);
}
