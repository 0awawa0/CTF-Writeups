import struct
import cryptography.hazmat.primitives.ciphers as ciphers
import cryptography.hazmat.backends as backends
import zlib


def parse_archive():
	files = {}

	with open("archive", "rb") as f:
		archive = f.read()

	index = 0
	header = archive[index:index + 8]
	index = index + 8

	print(b"Header: " + header)

	files_count = struct.unpack("I", archive[index:index + 4])[0]
	index = index + 4

	print(b"Count of files: " + str(files_count).encode())
	print()

	for i in range(files_count):
	
		filename_length = struct.unpack("I", archive[index:index + 4])[0]
		index = index + 4
		print(b"Filename length: " + str(filename_length).encode())

		filename = archive[index:index + filename_length]
		index = index + filename_length
		print(b"Filename: " + filename)

		uuid = archive[index: index+16]
		files[uuid] = {}
		files[uuid]["name"] = filename
		index = index + 16
		print(b"UUID: " + uuid)

		file_stat = struct.unpack("2I", archive[index: index + 8])
		index = index + 8
		file_size = file_stat[0]
		files[uuid]["size"] = file_size
		filemode = file_stat[1]
		print(b"File size: " + str(file_size).encode())
		print(b"File mode: " + str(filemode).encode())

		time = struct.unpack("3d", archive[index: index + 24])
		index = index + 24

		atime = time[0]
		mtime = time[1]
		ctime = time[2]
		print(b"atime: " + str(atime).encode())
		print(b"mtime: " + str(mtime).encode())
		print(b"ctime: " + str(ctime).encode())

		file_length = struct.unpack("I", archive[index: index + 4])[0]
		index = index + 4
		print(b"File length: " + str(file_length).encode())

		file_data = archive[index: index + file_length]
		index = index + file_length
		#print(b"File data: ")
		#print(file_data)

		with open(f"file{i}", "wb") as f:
			f.write(file_data)
		files[uuid]["data"] = file_data
		print()
	return files

# Parsing keystore
def parse_keystore():

	keys = {}
	with open("keys", "rb") as f:
		keystore = f.read()

	index = 0
	keystore_header = keystore[index: index + 8]
	index = index + 8
	print(b"Keystore header: " + keystore_header)

	keys_count = struct.unpack("I", keystore[index: index + 4])[0]
	index = index + 4
	print(b"Count of keys in the keystore: " + str(keys_count).encode())
	print()

	for i in range(16):

		uuid = keystore[index: index + 16]
		keys[uuid] = {}
		index = index + 16
		print(b"UUID: " + uuid)

		params = list(keystore[index: index + 32])
		index = index + 32
		params.reverse()
		init_vector = bytes(params[0:16])
		key = bytes(params[16:])
		keys[uuid]["init_vector"] = init_vector
		keys[uuid]["key"] = key
		print(b"init_vector: " + init_vector)
		print(b"key: " + key)

		dictionary_length = struct.unpack("I", keystore[index: index + 4])[0]
		index = index + 4
		print(b"dictionary length: " + str(dictionary_length).encode())

		substitution_dict = {}
		print(b"Dictionary: ")
		for j in range(dictionary_length):
			subst = struct.unpack("2I", keystore[index: index + 8])
			index = index + 8
			block_i = subst[0]
			block_j = subst[1]
			substitution_dict[block_j] = block_i 
			print(b"    " + str(block_i).encode() + b" -> " + str(block_j).encode())
			
		keys[uuid]["dictionary"] = substitution_dict
		print()
	return keys


def unpad(data):
	last_byte = data[-1]
	if data[len(data)-last_byte:] == bytes([last_byte]*last_byte):
		data = data[:len(data)-last_byte]
	return data


def decrypt(files, keys):
	backend = backends.default_backend()
	k = 0
	for i in files.keys():
		data = files[i]["data"]
		blocks_count = len(data) // 128
		blocks = [data[i * 128: (i + 1) * 128] for i in range(blocks_count)]
		unshuffled = bytes([])
		for j in range(blocks_count):
			unshuffled += blocks[keys[i]["dictionary"][j]]
		unshuffled = unpad(unshuffled)
		cipher = ciphers.Cipher(ciphers.algorithms.AES(keys[i]["key"]), ciphers.modes.CBC(keys[i]["init_vector"]), backend=backend)
		decryptor = cipher.decryptor()
		unshuffled = decryptor.update(unshuffled)
		unshuffled = unpad(unshuffled)

		with open(f"{k}.txt", "wb") as f:
			f.write(zlib.decompress(unshuffled))
		k += 1


if __name__ == "__main__":
	files = parse_archive()
	keys = parse_keystore()
	decrypt(files, keys)
