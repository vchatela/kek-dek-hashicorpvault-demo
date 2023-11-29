import hvac
import sys
import base64
from cryptography.fernet import Fernet

# Initialize the Vault Client (Replace with your Vault server URL and token)
sys.path.append('Z:\\tools_enc\\Vault')
from config import vault_addr, vault_role_id, vault_secret_id

client = hvac.Client(url=vault_addr)
client.auth.approle.login(
        role_id=vault_role_id,
        secret_id=vault_secret_id,
    )

# Check if HVAC client is authenticated
if not client.is_authenticated():
    print("Client is not authenticated")
    exit(-1)

# Vault Key Name
vault_key_name = 'kek_demo_key'

# Example of encoding data to base64
def encode_base64(data):
    return base64.b64encode(data).decode('utf-8')

# Example of decoding base64 data
def decode_base64(data):
    return base64.b64decode(data)

# Check if the key exists in Vault, if not, create it
def ensure_vault_key_exists():
    if not client.secrets.transit.read_key(name=vault_key_name,mount_point='transit-kek-demo')['data']['keys']:
        client.secrets.transit.create_key(name=vault_key_name,mount_point='transit-kek-demo')

# Function to generate a Data Encryption Key (DEK)
def generate_dek():
    return Fernet.generate_key()

# Function to encrypt data using DEK
def encrypt_data(data, dek):
    f = Fernet(dek)
    return f.encrypt(data)

# Function to decrypt data using DEK
def decrypt_data(encrypted_data, dek):
    f = Fernet(dek)
    return f.decrypt(encrypted_data)

# Updated encryption function
def vault_encrypt_dek(dek):
    encoded_dek = encode_base64(dek)  # Ensure DEK is base64-encoded
    encrypt_data = client.secrets.transit.encrypt_data(
        name='kek_demo_key',
        mount_point='transit-kek-demo',
        plaintext=encoded_dek
    )
    return encrypt_data['data']['ciphertext']

# Updated decryption function
def vault_decrypt_dek(encrypted_dek):
    decrypt_data = client.secrets.transit.decrypt_data(
        name='kek_demo_key',
        mount_point='transit-kek-demo',
        ciphertext=encrypted_dek
    )
    decoded_dek = decode_base64(decrypt_data['data']['plaintext'])  # Decode the decrypted DEK
    return decoded_dek

# Ensure the Vault key exists
ensure_vault_key_exists()

# Generate DEK
dek = generate_dek()

# Sample data to encrypt
sample_data = b"Hello, this is a test data!"

# Encrypt the data using DEK
encrypted_data = encrypt_data(sample_data, dek)

# Encrypt the DEK using KEK in Vault
encrypted_dek = vault_encrypt_dek(dek)

# Decrypt the DEK using KEK in Vault
decrypted_dek = vault_decrypt_dek(encrypted_dek)

# Decrypt the data using DEK
decrypted_data = decrypt_data(encrypted_data, decrypted_dek)

# Output the results
print("Encrypted Data:", encrypted_data)
print("Decrypted Data:", decrypted_data.decode())