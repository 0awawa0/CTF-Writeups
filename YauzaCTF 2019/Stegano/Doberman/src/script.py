with open("encrypted", 'rb') as f:
	data = f.read()
with open("key", 'rb') as f:
	key = f.read()

int_data = int.from_bytes(data, "big")
int_key = int.from_bytes(key, "big")
decr = int_data ^ int_key
decr = decr.to_bytes(decr.bit_length(), "big").strip(b"\x00")
print(decr.decode())