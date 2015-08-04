/*
 * Server to send mp4 video File
 *
 * Raphael
 */


#include <stdio.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <signal.h>
#include <string.h>
#include <stdlib.h>
#include <sys/types.h>
#include <unistd.h>
#include <netdb.h>

static void die(const char *msg)
{
    perror(msg);
    exit(1);
}

/*
 * argv:
 *
 * 1. video file/path to video file
 * 2. port
 *
 */


int main(int argc, char **argv)
{
    // server info
    int servSock; /* Socket descriptor for server */
    int clntSock; /* Socket descriptor for client */
    struct sockaddr_in myServAddr; /* Local address */
    struct sockaddr_in myClntAddr; /* Client address */
    unsigned short myServPort; /* port this server is running on */ 
    unsigned int clntLen; /* Length of client address data structure */

    myServPort = atoi(argv[2]); /* get server running on port specified by second arg */
    memset(&myServAddr, 0, sizeof(myServAddr)); // Zero out structure
    myServAddr.sin_family = AF_INET; // Internet address family
    myServAddr.sin_addr.s_addr = htonl(INADDR_ANY); // Any incoming interface
    myServAddr.sin_port = htons(myServPort); //local port

    /* create socket */
    if((servSock = socket(PF_INET, SOCK_STREAM, 0)) < 0)
        die("socket() failed");

    // Bind to local address
    if(bind(servSock, (struct sockaddr *)&myServAddr, sizeof(myServAddr)) <0)
    {
        die("bind() failed");
    }

    // listen
    if(listen(servSock, 5) < 0)
        die("listen() failed");

    // accept client response
    if((clntSock = accept(servSock, (struct sockaddr *) &myClntAddr, &clntLen)) < 0)
        die("accept() failed");



    FILE *fp = fopen(argv[1], "rb+");

    /*char *p = "0";
    //fprintf(stdout, "%s \n", p);
    char *k = malloc(sizeof(int) * 1440);
    int i;
    fprintf(stdout, "here \n");
    for(i = 0; i < 1440; i++)
    {
       k = strcat(k , p);
    }*/

    //fprintf(stdout, " p:  %s; k: %s  \n", p, k);

    fseek(fp, 0, SEEK_END);

    long int length_of_vid_bytes = ftell(fp);
    //long int length_of_vid_bits = length_of_vid_bytes / 8;
    

   // if(length_of_vid_bytes == length_of_vid_bits)
        //die("fuck \n");



    fseek(fp, 0, SEEK_SET);

    //int dist = 1440;


    fprintf(stdout, " length of vid: %ld  \n", length_of_vid_bytes);


    int count = 0;

    FILE* fpClnt = fdopen(clntSock, "wb+");
    if (fpClnt == NULL)
        die("fdopen failed");

    for( ; ; )
    {
        //fprintf(stderr, "here 1, %d  \n", length_of_vid_bits);
        fseek(fp, 0, SEEK_SET);
        char toSend[4096];
        int toCheck = 0;
        while((toCheck = fread(toSend, 1, sizeof(toSend), fp)) > 0)
        {
            //fprintf(stderr, "here \n");
            //fseek(fp, count, SEEK_SET);
            //fgets(toSend, 4096, fp);
            //fputs(toSend, fpClnt);
            //count += 4096;
            //
            size_t checkLength;
            int idx = ftell(fp);
            //fprintf(stderr, "%d \n", idx);

            int bits_from_end = length_of_vid_bytes - idx;

            //fprintf(stderr, "bits from end: %d \n", bits_from_end);
            //int bits_to_add = length_of_vid_bits - idx;
        
            if((checkLength = fwrite(toSend, 1, toCheck, fpClnt)) != toCheck)
            {
                /*fprintf(stdout, "here \n");
                if(bits_from_end == 0)
                {
                    fprintf(stdout, "bytes read %d, bytes written %zu", toCheck, checkLength);
                    break;
                }


                else if(bits_from_end > 4096)
                {
                    char b = '\0';
                    char *a = &b;
                    if(fwrite(a, 1, 1, fpClnt) < 0)
                        die("send 1 messed up");
                    continue;
                
                }

                else if(strlen(toSend) + idx != length_of_vid_bytes)
                {
                    fprintf(stdout, " length toSend: %ld bits from end %d, index %d", strlen(toSend), bits_from_end, idx);
                    fwrite(toSend, 1, strlen(toSend), fpClnt);
                    char b = '\0';
                    char *a = &b;
                    if(fwrite(a, 1, 1, fpClnt) < 0)
                        die("send 2  messed up");
                    
                    fseek(fp, strlen(toSend) + idx + 1, SEEK_SET);
                    continue;

                }      
            
                else {
                    //fwrite(toSend, 1, bits_from_end, fpClnt);
                    fprintf(stderr, "tripped \n");
                    break;
                }*/

                die("send messed up");
            }





            

            
        }
        break;




    }


    /*for(count = 1000;  count < length_of_vid_bits; count += 10)
    {
        fseek(fp, count, SEEK_SET);

       if(count % 1000 == 0)
        fputs("0000", fp);

        if(count == 20000)
            break;
        
        //dist += 1440;
    }*/

    //fseek(fp,70000, SEEK_SET);
    //fputs(k, fp); 


    fclose(fp);
    fclose(fpClnt);
    //free(k);



    
    return 0;
}




