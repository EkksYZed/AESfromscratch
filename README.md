# AESfromscratch
The purpose of this project is to implement the AES (Advanced Encryption Standard) algorithm to understand its encryption and decryption mechanisms. AES is a widely used block cipher encryption algorithm known for its security and efficiency. In this project, AES is applied with a block size of 16 bytes and a key size of 16 bytes, which results in 10 rounds of encryption.

AES operates in ECB (Electronic Codebook) mode, where each block of plaintext is encrypted independently. While ECB mode is straightforward, it has vulnerabilities such as revealing patterns in the encrypted data. For improved security, other modes like CBC (Cipher Block Chaining) are recommended.

Encryption Flow:
Plaintext Input: Convert plaintext into hexadecimal format.
Padding: Add padding to ensure the plaintext is a multiple of 16 bytes.
Key Expansion: Generate round keys from the original key.
Block Encryption: Divide the padded plaintext into 16-byte blocks and encrypt each block through 10 rounds:
Round 1: XOR the block with the round key, substitute bytes using the S-box, shift rows, and mix columns.
Rounds 2-9: Continue with substitution, shifting rows, and mixing columns.
Round 10: Perform the final XOR with the round key without mixing columns.
Result: Produce the encrypted ciphertext.
Decryption Flow:
Ciphertext Input: Use the ciphertext and the original key for decryption.
Key Expansion: Generate round keys from the original key.
Block Decryption: Divide the ciphertext into 16-byte blocks and decrypt each block through 10 rounds:
Round 1: XOR the block with the round key, reverse the mix columns operation, reverse the shift rows, and substitute bytes using the inverse S-box.
Rounds 2-9: Continue with reverse substitution, shifting rows, and reverse mixing columns.
Round 10: Perform the final XOR with the round key without reverse mixing columns.
Result: Obtain the original plaintext by removing padding.
Testing:
Generate Key: Create a random 16-byte key.
Encrypt Data: Encrypt plaintext using the generated key.
Decrypt Data: Decrypt the resulting ciphertext to verify that the original plaintext is recovered.
Security Considerations:
Key Management: Keep the encryption key secure and ensure it is randomly generated.
Mode of Operation: While ECB mode is used here, consider using more secure modes like CBC or CTR for practical applications.
Side-Channel Attacks: Be aware of potential information leaks through side-channel attacks and use additional security measures for authentication and integrity.
