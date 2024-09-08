# AES Project

## Purpose

The purpose of this project is to implement the AES (Advanced Encryption Standard) algorithm to understand its encryption and decryption mechanisms. AES is a widely used block cipher encryption algorithm known for its security and efficiency. In this project, AES is applied with a block size of 16 bytes and a key size of 16 bytes, resulting in 10 rounds of encryption.

## AES Operation

AES operates in **ECB (Electronic Codebook)** mode, where each block of plaintext is encrypted independently. While ECB mode is straightforward, it has vulnerabilities, such as revealing patterns in the encrypted data. For improved security, other modes like **CBC (Cipher Block Chaining)** are recommended.

## Encryption Flow

1. **Plaintext Input**: Convert plaintext into hexadecimal format.
2. **Padding**: Add padding to ensure the plaintext is a multiple of 16 bytes.
3. **Key Expansion**: Generate round keys from the original key.
4. **Block Encryption**:
   - **Rounds 1-9**:
     - XOR the block with the round key.
     - Substitute bytes using the S-box.
     - Shift rows.
     - Mix columns.
   - **Round 10**: Perform the final XOR with the round key without mixing columns.
5. **Result**: Produce the encrypted ciphertext.

## Decryption Flow

1. **Ciphertext Input**: Use the ciphertext and the original key for decryption.
2. **Key Expansion**: Generate round keys from the original key.
3. **Block Decryption**:
   - **Rounds 1-9**:
     - XOR the block with the round key.
     - Reverse the mix columns operation.
     - Reverse the shift rows.
     - Substitute bytes using the inverse S-box.
   - **Round 10**: Perform the final XOR with the round key without reverse mixing columns.
4. **Result**: Obtain the original plaintext by removing padding.

## Testing

1. **Generate Key**: Create a random 16-byte key.
2. **Encrypt Data**: Encrypt plaintext using the generated key.
3. **Decrypt Data**: Decrypt the resulting ciphertext to verify that the original plaintext is recovered.

## Security Considerations

1. **Key Management**: Keep the encryption key secure and ensure it is randomly generated.
2. **Mode of Operation**: While ECB mode is used here, consider using more secure modes like CBC or CTR for practical applications.
3. **Side-Channel Attacks**: Be aware of potential information leaks through side-channel attacks and use additional security measures for authentication and integrity.
