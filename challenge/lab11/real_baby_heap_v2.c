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

char **heap = NULL;
void menu(){
	puts("#########################");
	puts("    Real baby heap v2     ");
	puts("#########################");
	puts(" 1. Allocate            ");
	puts(" 2. Free                ");
	puts(" 3. Show                ");
	puts(" 4. Fill                ");
	puts(" 5. Exit                ");
	puts("#########################");
	printf("Your choice:");
}


void allocate(){
	size_t size ;
	for(int i = 0 ; i < 10 ; i++){
		if(!heap[i]){
			printf("Size:");
			size = read_long();
			if(size > 0x78){
				puts("too large");
				exit(-2);
			}
			heap[i] = malloc(size);
			if(!heap[i]){
				puts("Error!");	
			}
			return ;
		}
	}
	puts("Too more !");
}

void dfree(){
	unsigned int idx = 0 ;
	printf("Index:");
	idx = read_long();
	if(idx < 10){
		free(heap[idx]);
		heap[idx] = NULL ;	
	}else{
		puts("Too large");
	}
}

void show(){
	unsigned int idx = 0 ;
	printf("Index:");
	idx = read_long();
	if(idx < 10){
		if(heap[idx]){
			printf("Content:%s\n",heap[idx]);
		}
	}else{
		puts("Too large");
	}
}

void edit(){
	unsigned int idx = 0 ;
	printf("Index:");
	idx = read_long();
	if(idx < 10){
		if(heap[idx]){
			printf("Content :");
			gets(heap[idx]);
		}else{
			puts("Can not found the heap !");
		}
	}else{
		puts("Too large");
	}

}


int main(){
	init_proc();
	heap = malloc(10*sizeof(char*));
	while(1){
		menu();
		switch(read_long()){
			case 1:
				allocate();
				break ;
			case 2:
				dfree();
				break ;
			case 3:
				show();
				break ;
			case 4:
				edit();
				break ;
			case 5:
				exit(0);
				break ;
			default:
				puts("Invalid choice");
				break;
		}
	}
}
