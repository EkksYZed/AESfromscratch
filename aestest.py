from aesencrypt import *
from aesdecrypt import *

def aes_test():

    key = keygenerate()
    print("Secret Key",key)
    plaintext = input("Enter plaintext: ")


    ciphertext = aes_encrypt(plaintext, key)
    print("Ciphertext:", ciphertext)

    print(key)
    decrypted_text = aes_decrypt(ciphertext, key)
    print("Decrypted Text:", decrypted_text)

if __name__ == "__main__":
    aes_test()
