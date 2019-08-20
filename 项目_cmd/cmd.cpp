#include <stdio.h>
#include <sys/wait.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <stdlib.h>
#include <iostream>
#include <errno.h>
#include <limits.h>
#include <strings.h>
#include <cstring>

using namespace std;

#ifdef  OPEN_MAX
static long openmax = OPEN_MAX;
#else
static long openmax = 0;
#endif

/*
 * If OPEN_MAX is indeterminate, we're not
 * guaranteed that this is adequate.
 */
#define OPEN_MAX_GUESS 256

#define    SHELL    "/bin/sh"

long
open_max(void) {            //get system open max file number
    if (openmax == 0) {      /* first time through */
        errno = 0;
        if ((openmax = sysconf(_SC_OPEN_MAX)) < 0) {
            if (errno == 0)
                openmax = OPEN_MAX_GUESS;    /* it's indeterminate */
            else
                printf("sysconf error for _SC_OPEN_MAX");
        }
    }

    return (openmax);
}

static pid_t *childpid = NULL;
/* ptr to array allocated at run-time */
static int maxfd;    /* from our open_max(), {Prog openmax} */




FILE *
my_popen(const char *cmdstring, const char *type, timeval *timeout) {
    int i, pfd[2];
    pid_t pid;
    FILE *fp;

    /* only allow "r" or "w" */
    if ((type[0] != 'r' && type[0] != 'w') || type[1] != 0) {
        errno = EINVAL;        /* required by POSIX.2 */
        return (NULL);
    }

    if (childpid == NULL) {        /* first time through */
        /* allocate zeroed out array for child pids */
        maxfd = open_max();
        childpid = (pid_t *) (calloc(maxfd, sizeof(pid_t)));        //ask for memory
        if (childpid == NULL)
            return (NULL);
    }

    if (pipe(pfd) < 0)
        return (NULL);    /* errno set by pipe() */

    if ((pid = fork()) < 0)
        return (NULL);    /* errno set by fork() */
    else if (pid == 0) {                            /* child */
        if (*type == 'r') {
            close(pfd[0]);
            if (pfd[1] != STDOUT_FILENO) {
                cout<<"pfd[1] is "<<pfd[1]<<endl;
                dup2(pfd[1], STDOUT_FILENO);
                close(pfd[1]);
            }
        } else {
            close(pfd[1]);
            if (pfd[0] != STDIN_FILENO) {
                dup2(pfd[0], STDIN_FILENO);
                close(pfd[0]);
            }
        }

        /* close all descriptors in childpid[] */
        for (i = 0; i < maxfd; i++)
            if (childpid[i] > 0)
            {
                cout<<"child pid "<<childpid[i]<<" is alive"<<endl;
                close(i);
            }

        execl(SHELL, "sh", "-c", cmdstring, (char *) 0);

        _exit(127);
    }


    /* parent */
    cout << "###############################" << endl;
    cout << "pid is: " << pid << endl;
    fd_set fdset;
    FD_ZERO(&fdset);
    if (*type == 'r') {
        close(pfd[1]);
        int error;
        FD_SET(pfd[0], &fdset);

        error = select(pfd[0] + 1, &fdset, nullptr, nullptr, timeout);
        if (error == 0) {
            cout << "error,time over" << endl;
            if (waitpid(pid, nullptr, WNOHANG) == 0) {

                if (kill(pid, SIGKILL) != 0)
                    cout << "kill failed" << endl;

                if (wait(nullptr) != pid)            //wait for child
                {
                    cout << "error in wait pid - after kill child" << endl;
                }

            }
            return nullptr;
        } else if (error == -1) {       //QE
            cout << "error in select" << endl;
            if (wait(nullptr) != pid)            //wait for child
            {
                cout << "error in wait pid" << endl;
            }
            return nullptr;

        } else {

            if (FD_ISSET(pfd[0], &fdset)) {
                FILE *fp;
                fp = fdopen(pfd[0], "r");
                childpid[fileno(fp)] = pid;    /* remember child pid for this fd */
                return fp;
            }

        }

    }
    //TODO:if(type=='w')

    return nullptr;
}



int
pclose(FILE *fp) {

    int fd, stat;
    pid_t pid;

    if (childpid == NULL)
        return (-1);        /* my_popen() has never been called */

    fd = fileno(fp);
    
    if ((pid = childpid[fd]) == 0)
        return (-1);        /* fp wasn't opened by popen() */

    childpid[fd] = 0;           //map pid <-> fd
    if (fclose(fp) == EOF)
        return (-1);
    

    
    while ( waitpid(pid, &stat, 0) < 0)
    {
        cout<<"waitpid < 0"<<endl;
        if (errno != EINTR)
            return (-1);    /* error other than EINTR from waitpid() */
    }
    
    return (stat);    /* return child's termination status */
}





int run_command(char *cmd, int cmd_length, char *buffer, int buffer_length, int timeout) {
    FILE *fp;
    timeval timeout_para;
    timeout_para.tv_sec = timeout;       //set timeout
    timeout_para.tv_usec = 0;

    fp = my_popen(cmd, "r", &timeout_para);
    if (fp == nullptr) {
        cout << "error in my_popen" << endl;
        return -1;
    }

    memset(buffer, 0, buffer_length);
    int rsize = fread(buffer, 1, buffer_length, fp);
    if (rsize <= 0) {
        strncpy(buffer, "******execute command fail **********\n", buffer_length);
        return -1;
    }

    int temp_int = pclose(fp);
    cout << "exit code is: " << temp_int << endl;
    return 0;
}


int main() {
    char cmd[100];
    char buffer[1000];
    int timeout = 100;
    int cmd_length = sizeof(cmd);
    int buffer_length = sizeof(buffer);
    while (1) {
        cout << "$" << endl;
        memset(cmd, 0, cmd_length);
        if (read(STDIN_FILENO, cmd, cmd_length) < 0) {
            cout << "error in input" << endl;
            continue;
        }
        cout << "cmd is : " << cmd << endl;
        memset(buffer, 0, buffer_length);
        if (run_command(cmd, cmd_length, buffer, buffer_length, timeout) == 0) {
            cout << "###############################" << endl;
            cout << buffer << endl;
        } else
            continue;
    }
}