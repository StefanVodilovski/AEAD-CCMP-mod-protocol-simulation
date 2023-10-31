import base64
from importlib.machinery import FrozenImporter
import string
import time
from clear_text_frame import Clear_Text_frame
from encrypted_frame import Encrypted_frame
from Crypto.Random import get_random_bytes
from Crypto.Protocol.KDF import PBKDF2

from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad


def chunk_data(data):
    if isinstance(data, str):
        data = data.encode("utf-8")
    chunks = []
    while True:
        if len(data) > 128:
            chunks.append(data[:128])
            data = data[128:]
        else:
            chunks.append(data)
            return chunks


def encrypt_data(clear_frame, iv, aes_cipher):
    # creating iv and aes cipher
    data_chunks = chunk_data(clear_frame.data)
    result_data = b""
    for i in range(len(data_chunks)):
        count_representation = format(i + 1, "03d")
        ctr_preload = iv[:125] + count_representation.encode("utf-8")
        ciphered_data = aes_cipher.encrypt(pad(ctr_preload, 32))
        xor = bytes([a ^ b for a, b in zip(ciphered_data, data_chunks[i])])
        result_data += xor
    return result_data


def calculated_mic(clear_frame, iv, aes_cipher):
    mic = ""
    salt = b"\xb2\x16\xe8\xef\xca\xe02\xd6\x80\xb6\xd0\x02\x80(\xe64Sd+oZ\xce\xaf\x9e.Q\x9d\xe3{\xb3P\x97"
    password = "apassword"
    key = PBKDF2(password, salt, dkLen=32)

    inital_cipher = AES.new(key, AES.MODE_ECB)

    encrypted_iv = aes_cipher.encrypt(pad(iv, 32))
    # xor = encrypted_iv ^ clear_frame.get_source_addr().encode("utf-8")

    source_address_encoded = clear_frame.get_source_addr().encode("utf-8")
    xor = bytes([a ^ b for a, b in zip(encrypted_iv, source_address_encoded)])
    encrypt_xor = inital_cipher.encrypt(pad(xor, AES.block_size))

    # xor = encrypt_xor ^ clear_frame.get_dest_addr().encode("utf-8")
    destination_address_encoded = clear_frame.get_dest_addr().encode("utf-8")
    xor = bytes([a ^ b for a, b in zip(encrypt_xor, destination_address_encoded)])
    data_chunks = chunk_data(clear_frame.data)

    for i in range(len(data_chunks)):
        encrypt_xor = inital_cipher.encrypt(pad(xor, 32))
        # xor = encrypt_xor ^ data_chunks[i].encode("utf-8")
        xor = bytes([a ^ b for a, b in zip(encrypt_xor, data_chunks[i])])

    resulting_mic = inital_cipher.encrypt(pad(xor, 32))
    zero = 0
    zero_representation = format(zero, "03d")
    pl_zero = iv[:125] + zero_representation.encode("utf-8")
    # resulting_mic_xor = pl_zero ^ resulting_mic
    resulting_mic_xor = bytes([a ^ b for a, b in zip(pl_zero, resulting_mic)])
    return resulting_mic_xor


def decrypt_frame(encrypted_frame, iv, aes_cipher):
    payload = encrypted_frame.get_encrypted_data()
    chunked_payload = chunk_data(payload)
    # Define the salt and generate the key

    result_data = b""
    for i in range(len(chunked_payload)):
        count_representation = format(i + 1, "03d")
        ctr_preload = iv[:125] + count_representation.encode("utf-8")
        ciphered_data = aes_cipher.encrypt(pad(ctr_preload, 32))
        xor = bytes([a ^ b for a, b in zip(ciphered_data, chunked_payload[i])])
        result_data += xor

    return result_data


def encyption_proccess(source_address, destination_adress, data):
    clear_frame = Clear_Text_frame(data, source_address, destination_adress)
    iv = get_random_bytes(128)

    salt = b"\xb2\x16\xe8\xef\xca\xe02\xd6\x80\xb6\xd0\x02\x80(\xe64Sd+oZ\xce\xaf\x9e.Q\x9d\xe3{\xb3P\x97"
    password = "apassword"
    key = PBKDF2(password, salt, dkLen=32)
    inital_cipher = AES.new(key, AES.MODE_ECB)

    encrypted_frame = Encrypted_frame(
        source_address,
        destination_adress,
        encrypt_data(clear_frame, iv, inital_cipher),
        calculated_mic(clear_frame, iv, inital_cipher),
    )

    print("your data will now we encrypted, please wait a few seconds :)")
    time.sleep(5)
    print("...")
    time.sleep(5)
    print("data is still encypting, this isn't easy be patient :D")
    time.sleep(5)
    print("it took a while but this is how your data looks in hex:")
    print(encrypted_frame.get_encrypted_data().hex())
    print("and this is your calculated mic also in hex:")
    print(encrypted_frame.get_mic().hex())
    return encrypted_frame, iv, inital_cipher


if __name__ == "__main__":
    source_address = input("Please enter source mac address: ")
    destination_adress = input("please enter destination mac address: ")
    data = input("input the data you want to send: ")
    # source_address = "2C:54:91:88:C9:E3"
    # destination_adress = "7A:21:55:B1:32:D1"
    # data = "this data will be encrypted and won't look like this in the encrypted frame"

    encrypted_frame, iv, inital_cipher = encyption_proccess(
        source_address, destination_adress, data
    )

    y_n = input(
        "do you want me to decrypted for you to see if it is really your data? y/n\n"
    )
    if y_n == "y":
        print("wait a few seconds now")
        time.sleep(5)
        print("this time i was fast , this is your data:")
        print(decrypt_frame(encrypted_frame, iv, inital_cipher).decode("utf-8"))
    # print(encrypted_frame.get_encrypted_data().hex())
    # print(encrypted_frame.get_mic().hex())

    # print(decrypt_frame(encrypted_frame, iv, inital_cipher).decode("utf-8"))

    # Encode the decrypted data in Base64
