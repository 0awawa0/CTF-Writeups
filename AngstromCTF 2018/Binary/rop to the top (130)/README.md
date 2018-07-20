# rop to the top

## Description

Here's some binary and source. Navigate to /problems/roptothetop/ on the shell server to try your exploit out!

hint: Look up "Return Oriented Programming" (ROP) vulnerabilities
and figure out how you might be able to change the return address.

## Solving

First, as always, I ran the binary. Here is what I saw:
<pre><font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># mv ./rop_to_the_top32 ./rop32
<font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./rop32
Usage: ./rop_to_the_top32 &lt;inputString&gt;
<font color="#EF2929"><b>root@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./rop32 &quot;some string&quot;
Now copying input...
Done!
</pre>

So the program takes one string argument and just does something with it. Now let's seee the source code.
```C
#include <stdlib.h>
#include <string.h>
#include <stdio.h>

void the_top(){

    system("/bin/cat flag");

}

void fun_copy(char *input){

    char destination[32];
    strcpy(destination, input);
    puts("Done!");
}

int main (int argc, char **argv){
    gid_t gid = getegid();
    setresgid(gid,gid,gid);

    if (argc == 2){
        puts("Now copying input...");
        fun_copy(argv[1]);
    } else {
        puts("Usage: ./rop_to_the_top32 <inputString>");
    }

    return 0;
}
```

The program is actually copies the input to the buffer (destination variable). Still, as I can see, there is no limitation for the input, but the buffer has only 32 bytes of length. So, I can overflow the buffer. Another important thing is that there is a function "the_top" which actually prints the flag. Now I need to figure out how can I use the buffer overflowing to call "the_top", so I can get the flag.

I decided to look this program in the IDA.
