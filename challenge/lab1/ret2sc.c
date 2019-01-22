#include <stdio.h>

char Name[10];

int main(){
	setvbuf(stdout,0,2,0);
	printf("Name:");
	read(0,Name,10);
	char buf[10];
	printf("Try your best:");
	gets(buf);
	return ;
}
