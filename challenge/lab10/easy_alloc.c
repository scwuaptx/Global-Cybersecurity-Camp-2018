#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>
#define TIMEOUT 60

void handler(int signum){
	puts("Timeout");
	_exit(1);
} 

void init_proc(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	signal(SIGALRM,handler);
	alarm(TIMEOUT);
} 

long long read_long(){
	char buf[24];
	long long choice ;
	__read_chk(0,buf,23,24);
	choice = atoll(buf);
	return choice;
}
 
void read_input(char *buf,unsigned int size){
	int ret ;
	ret = __read_chk(0,buf,size,size);
	if(ret <= 0){
		puts("read error");
		_exit(1);
	}
	if(buf[ret-1] == '\n')
		buf[ret-1] = '\x00';
} 

struct e {
	void (*hello)();
} ;

void menu(){
	puts("************************");
	puts("       Easy Alloc       ");
	puts("************************");
	puts(" 1. Alloc               ");
	puts(" 2. Magic               ");
	puts(" 3. Exit                ");
	puts("************************");
	printf("Your choice:");
}

void helloworld(){
	puts("hello world");
}

void l33t(){
	system("/bin/sh");
}

char *data = NULL;
void alloc(){
	size_t size = 0;
	printf("Size:");
	size = read_long();
	data = malloc(size);
	if(data){
		printf("data:");
		gets(data);
	}else{
		puts("error!");
		exit(-1);
	}
	printf("Your input is %s\n",data);
}

void magic(struct e *pp){
	pp->hello();
}



int main(){
	init_proc();
	struct e *p = malloc(sizeof(struct e));
	p->hello = helloworld;
	while(1){
		menu();
		switch(read_long()){
			case 1:
				alloc();
				break ;
			case 2:
				magic(p);
				break ;
			case 3:
				exit(0);
				break ;
			default:
				puts("Invalid choice");
				break;
		}
	}
}


