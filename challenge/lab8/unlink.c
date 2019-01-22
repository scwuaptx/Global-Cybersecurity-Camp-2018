#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>
#include <sys/mman.h>
#include <stdlib.h>
#include <signal.h>
#include <time.h>
#define TIMEOUT 60

void handler(int signum){
	puts("Timeout");
	_exit(1);
} 
struct chunk{
	size_t prev_size;
	size_t size;
	struct chunk *fd ;
	struct chunk *bk ;
};

struct chunk *bin = NULL ;
char *heapaddr = NULL;
char *top = NULL;
size_t heapsize = 0x10000 ;
void init_proc(){
	setvbuf(stdin,0,2,0);
	setvbuf(stdout,0,2,0);
	setvbuf(stderr,0,2,0);
	heapaddr = mmap(0x41410000,heapsize,PROT_READ|PROT_WRITE,MAP_PRIVATE|MAP_ANONYMOUS , -1,0);
	top = heapaddr ;
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

void ulink(struct chunk *p){
	if(bin->fd == bin){
		bin = NULL ;
	}else{
		if(p == bin){
			bin = bin->fd;
		}
		p->fd->bk = p->bk;
		p->bk->fd = p->fd;

	}
}

void menu(){
	puts("########################");
	puts("         unlink         ");
	puts("########################");
	puts(" 1. Allocate            ");
	puts(" 2. Free                ");
	puts(" 3. Show                ");
	puts(" 4. Fill                ");
	puts(" 5. Exit                ");
	puts("########################");
	printf("Your choice:");
}
char* my_malloc(size_t nb){
	struct chunk *victim = NULL;
	if(bin){
		victim = bin;
		while(victim->size != (nb+0x10)){

			if(victim->fd == bin)
				break ;
			victim = victim->fd ;
		}
		if(victim->size == (nb+0x10)){
			ulink(victim);
			return (char*)((long)victim+0x10);
		}

	}

	if(nb + 0x10 > heapsize){
		exit(-1);
	}else{
		victim = top;
		victim->size = nb+0x10;
		top += (nb + 0x10);
		return (char*)((long)victim+0x10);
	}
	
}

void my_free(char *ptr){
	struct chunk *victim ;
	struct chunk *next ;
	struct chunk *prev ;
	if(ptr == NULL)
		return ;
	victim = (long)(ptr - 0x10) ;
	if(bin){
		victim->fd = bin;
		victim->bk = bin->bk;
		bin->bk->fd = victim;
		bin->bk = victim;
		bin = victim;
	}else{
		bin = victim;
		victim->bk = victim->fd = victim;
	}
}

char *heap[10];

void allocate(){
	size_t size ;
	for(int i = 0 ; i < 10 ; i++){
		if(!heap[i]){
			printf("Size:");
			size = read_long();
			heap[i] = my_malloc(size);
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
		my_free(heap[idx]);
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
		}
	}
}

int main(){
	init_proc();
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
