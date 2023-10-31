a = "sdad"

type(a)


byte_data = b"0123456789ABCDEF" * 8  # Just an example bytes data

# Get the length of the bytes data
num_bytes = len(byte_data)
print(byte_data)
print(len(byte_data))
byte_data = byte_data[100:]
print(byte_data)
print(len(byte_data))
print(f"There are {num_bytes} bytes in the data.")
