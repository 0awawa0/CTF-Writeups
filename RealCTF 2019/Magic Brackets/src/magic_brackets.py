import socket

1001101
1001101

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