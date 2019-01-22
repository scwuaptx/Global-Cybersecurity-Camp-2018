#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>



int main(){
	char buf[0x20];
	setvbuf(stdin,0,_IONBF,0);
	setvbuf(stdout,0,_IONBF,0);
	printf("Data:");
	read(0,buf,0x100);
}
