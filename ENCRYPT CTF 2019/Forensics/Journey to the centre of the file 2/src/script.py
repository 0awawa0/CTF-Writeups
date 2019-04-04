import gzip
import bz2
import zipfile

while 1:
	try:
		with zipfile.ZipFile("flag") as z:
			z.extractall()
	except:
		with open("flag", "rb") as f:
			data = f.read()
			try:
				data = gzip.decompress(data)
				with open("flag", "wb") as f:
					f.write(data)
			except:
				try:
					data = bz2.decompress(data)
					with open("flag", "wb") as f:
						f.write(data)
				except:
					print(data)
					break
