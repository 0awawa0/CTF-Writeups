import zipfile

with zipfile.ZipFile("flag") as f:
	f.extractall()