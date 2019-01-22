#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>

char username[48];

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

int check(char *str){
	int i ;
	for(i = 0 ; i < strlen(str) ; i++){
		if(!isalnum(str[i])){
			return 0;
		}
	}
	return 1;
}

void WriteSomething(char *addr){
	printf("data :");
	read_input(addr,0x8);
	puts("done !");
}


int main(){
	char buf[0x20];
	setvbuf(stdin,0,_IONBF,0);
	setvbuf(stdout,0,_IONBF,0);
	printf("What's your name :");
	read_input(username,48);
	if(check(username)){
		printf("Where do you want to write :");
		read_input(buf,0x18);
		WriteSomething((char*)strtoll(buf,0,16));
	}

}
