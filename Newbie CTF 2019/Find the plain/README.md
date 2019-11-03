# Find the plain

## Task

![task](./src/task.png)

[vithim.pcapng](./src/vithim.pcapng)

## Solution

Here I have the network traffic dump. I loaded it to Wireshark and used filter `ftp || ftp-data` as for in the task was said that data was sent with FTP.

![filter](./src/filter.png)

Next, I followed the TCP stream and found the password.

![password](./src/password.png)

Now I need to find the data. So I looked at FTP-DATA packet.

![ftp-data](./src/ftp_data.png)

Here I see some Base64 encoded string. Decoding it...

![from_base](./src/from_base.png)

Got the URL.

![data](./src/data.png)

And now I have the data. But the system won't accept the flag `KorNewbie{root_k459iki6m5j094m2lmkhjmi9527l81ml}`. Seems like I did something wrong. Let's dig some deeper.

Looking at expert information I found this fascinating comment

![comment](./src/comment.png)

Ok, now I decrypt the data

![decrypt](./src/decrypt.png)

The flag must be `KorNewbie{root_d459bdb6f5c094f2efdacfb9527e81fe}`, although I can't check it because the CTF have been paused for a 15 hours by now =)
