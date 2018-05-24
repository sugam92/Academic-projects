#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <string.h>

int main(int argc, char *argv[]){
char message[100000];
int server, portNumber;
socklen_t len;
struct sockaddr_in servAdd;
if(argc != 3){
  printf("Call model:%s <IP> <Port#>\n",argv[0]);
  exit(0);
}
if ((server=socket(AF_INET,SOCK_STREAM,0))<0){
  fprintf(stderr, "Cannot create socket\n");
  exit(1);
}
servAdd.sin_family = AF_INET;

sscanf(argv[2], "%d", &portNumber);

servAdd.sin_port = htons((uint16_t)portNumber);

if(inet_pton(AF_INET, argv[1],&servAdd.sin_addr) < 0){
  fprintf(stderr, " inet_pton() has failed\n");
  exit(2);
}
if(connect(server, (struct sockaddr *) &servAdd,sizeof(servAdd))<0){
  fprintf(stderr, "connect() failed, exiting\n");
  exit(3);
}
while(1){

  printf("Command:");
	scanf("%[^\n]%*c", &message[0]);
	send(server, message, strlen(message), 0);

  if(strcmp(message, "quit") == 0){
		close(server);
		printf("Quit by User\n");
		exit(1);
	}

  if(recv(server, message, 100000, 0) >= 0){
		printf("Server's Response: %s\n", message);
		bzero(message, sizeof(message));
	}

}
}
