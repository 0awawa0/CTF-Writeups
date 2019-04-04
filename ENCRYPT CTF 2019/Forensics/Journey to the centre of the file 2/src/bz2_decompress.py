import bz2

with open('ziptunnel2', "rb") as f:
	data = f.read()

data = bz2.decompress(data)

with open("flag", "wb") as f:
	f.write(data)