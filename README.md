# README: Cryptographic Choices and Implementation

## Overview
This document explains the cryptographic choices and implementation details for a Python script that integrates HashiCorp Vault for Key Encryption Key (KEK) management. The script demonstrates encrypting data using a Data Encryption Key (DEK) and securing the DEK using a KEK stored in HashiCorp Vault.

## Cryptographic Choices

### 1. Data Encryption Key (DEK)
- **Type**: Symmetric Key
- **Algorithm**: AES (Advanced Encryption Standard) via Fernet
- **Reasoning**: 
  - **Performance**: Symmetric key algorithms like AES are generally faster than asymmetric algorithms, making them suitable for encrypting and decrypting large amounts of data.
  - **Simplicity**: Using Fernet simplifies the implementation by handling aspects like key generation, initialization vector (IV) management, and data integrity (via HMAC).

### 2. Key Encryption Key (KEK)
- **Type**: Asymmetric Key
- **Algorithm**: RSA (Rivest–Shamir–Adleman)
- **Managed By**: HashiCorp Vault (Transit Secret Engine)
- **Reasoning**:
  - **Security**: Asymmetric cryptography provides a higher level of security, appropriate for protecting the DEK.
  - **Separation of Concerns**: By using asymmetric keys for KEK, we separate the encryption of data (handled by the DEK) from the encryption of the key itself, adding an extra layer of security.
  - **Management**: HashiCorp Vault offers robust key management capabilities like access controls, audit logs, and automatic key rotation.

### 3. Use of HashiCorp Vault
- **Purpose**: Securely store and manage KEK.
- **Capabilities**:
  - **API-Based Access**: Enables programmatically accessing and managing cryptographic keys.
  - **Scalability and Flexibility**: Supports various cryptographic operations and scaling as per application needs.
  - **Security and Compliance**: Ensures secure key storage and compliance with industry standards.

## Implementation Details

### Script Workflow
1. **Key Initialization**:
   - Check if the KEK (`kek_demo_key`) exists in Vault. If not, create it.
2. **DEK Generation**:
   - Generate a symmetric key (DEK) for data encryption.
3. **Data Encryption**:
   - Encrypt sample data using the DEK.
4. **DEK Encryption**:
   - Encrypt the DEK using the KEK stored in Vault.
5. **DEK Decryption**:
   - Decrypt the DEK using the KEK for data decryption.
6. **Data Decryption**:
   - Decrypt the data using the decrypted DEK.

### Libraries and Tools
- **Cryptography**: Provides cryptographic primitives and utilities in Python.
- **HVAC**: HashiCorp Vault API client for Python, used for interacting with Vault.
- **HashiCorp Vault**: Manages the KEK and provides encryption/decryption services via its Transit Secret Engine.

## Security Considerations
- Ensure secure communication with Vault (use HTTPS in production).
- Properly handle and protect Vault access tokens and secrets.
- Regularly audit and rotate cryptographic keys.

## Conclusion
This implementation demonstrates a secure way to encrypt data using a combination of symmetric and asymmetric cryptography, with the added security and management benefits of HashiCorp Vault. It serves as a blueprint for applications requiring secure data encryption and robust key management.