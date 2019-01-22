#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

void See_something(void *addr){
	unsigned long long *address ;
	address = (unsigned long long *)addr ;
	printf("The content of the address : %p\n",*address);
};

int main(){
	setvbuf(stdout,0,2,0);
	char address[10] ;
	char message[256];
	unsigned int addr ;
	puts("###############################");
	puts("Do you know return to library ?");
	puts("###############################");
	puts("What do you want to see in memory?");
	printf("Give me an address (in hex) :");
	read(0,address,10);
	addr = strtoll(address,0,16);
	See_something(addr) ;
	printf("Leave some message for me :");
	gets(message);
	printf("%s\n",message);
	puts("Thanks you ~");
	return 0 ;
}
