#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <time.h>
#include <string.h>

void serviceClient(int client){
  char buffer[100000];
  while(1){
    recv(client, buffer, 100000, 0);
    if(strcmp(buffer, "quit") == 0){
      //printf("Quit by User\n");
		exit(1);
    }else{
      system(buffer);
	  //fprintf(stderr, "Clent send back: %s\n", buffer);
      bzero(buffer, sizeof(buffer));
    }
  }

}
int main(int argc, char *argv[]){

int sd, client, pno,status;
socklen_t len;
struct sockaddr_in address_server;
struct sockaddr_in address_server_new;
if(argc != 2){
  fprintf(stderr,"Call model: %s <Port#>\n",argv[0]);
  exit(0);
}

if((sd = socket(AF_INET, SOCK_STREAM, 0))<0){
  fprintf(stderr, "SOCKET ERROR: Could not create socket\n");
  exit(1);
}

memset(&address_server, '\0', sizeof(address_server));

address_server.sin_family = AF_INET;

address_server.sin_addr.s_addr = INADDR_ANY;

sscanf(argv[1], "%d", &pno);

address_server.sin_port = htons((uint16_t)pno);

if(bind(sd, (struct sockaddr *) &address_server,sizeof(address_server))<0){
  printf("Failed to bind\n");
  exit(1);
}


if(listen(sd, 5)==0){
  printf("Waiting for connections....\n");
}else{
  printf("Failed to listen.\n");
}

while(1){
  if((client=accept(sd,(struct sockaddr*)&address_server_new,&len))<0){
    exit(1);
  }
  else
	  fprintf(stderr,"Conneted to Client on Port# %d\n",pno);
  if(!fork()){
    close(sd);
    dup2( client, STDOUT_FILENO );
    dup2( client, STDERR_FILENO );
    serviceClient(client);
  }
}
wait(&status);

}

