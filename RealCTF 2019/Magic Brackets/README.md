# Magic Brackets

## Task

![task](./src/task.png)

[app.py](./src/app.py)

## Solution

First, I looked at the source code of the application:

```Python
import random

print("Welcome, traveller!")
print("I have a task for you.")
print("I will give you some numbers.")
print("The only thing you have to do is send them back to me.")
print("If you do everything correctly, I will give you the flag.")
print("Sounds easy, right?")
print("However, to prove that you are the true bracket master, you can only use the following symbols: ()[]<>|")
print("Well here we go:")

for _ in range(100):
    num = random.randint(100, 100000)
    print(num)
    try:
        if num != eval("".join([c for c in input() if c in "()[]<>|"])):
            print("Sorry, that's wrong :c")
            exit(0)
    except:
        print("Ouch, that hurts :c")
        exit(0)
print("Good job!")
print("Your flag is [REDACTED]")
```

So, we need to enter the string, which contains only symbols from this list: `()[]<>|`. Okay. I was confused for a while. But after about an hour and a half I came up with this code:

```Python
>>> [()] > []
True
```

Ha, I made 1. But I need numbers in range 100..100000. Now I remembered about bit shifts. And here we go:

```Python
>>> ([()] > []) << ([()] > [])
2
```

Yeah! Now, shifting this, I can get any number 2<sup>n</sup>. And las thing left is to get any number `2 % n != 0`. Luckily, I can use `|`. So I can use it to make any uneven number:

```Python
>>> ([()] > []) << ([()] > []) | ([()] > [])
3
```

Using all these things I made this code to solve the task:

```Python
import socket


def to_brackets(number: int):
	bint = bin(number)[2:]
	one = "([()]>[])"
	result = one
	for bit in bint[1:]:
		if bit == "1":
			result = f"(({result}) << ({one})) | {one}"
		else:
			result = f"(({result}) << ({one}))"
	return result


def main():
	s = socket.socket()
	s.connect(("tasks.realctf.pro", 28392))
	print(s.recv(1024).decode())
	while 1:
		data = s.recv(1024).decode()
		print(data)
		try:
			num = int(data.strip())
			res = to_brackets(num) + "\n"
			print(res)
			s.send(res.encode())
		except:
			break
	print(to_brackets(543))


if __name__ == "__main__":
	main()
```

Run it and here we go:

![flag](./src/flag.png)

Flag: `HSE{8RrrR4cK3t_P0O0w3rrr}`