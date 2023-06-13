from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import (
    decode_dss_signature, encode_dss_signature)
from cryptography.hazmat.primitives.serialization import (
    Encoding, PublicFormat)
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import serialization


# Generate a new ECDSA key pair
private_key = ec.generate_private_key(ec.SECP256R1())

# Get the corresponding public key
public_key = private_key.public_key()

# Serialize the public key
public_key_pem = public_key.public_bytes(Encoding.PEM, PublicFormat.SubjectPublicKeyInfo)

# Load a private key from PEM-encoded data
# private_key = load_pem_private_key(pem_data, password=None)

# Sign a message using the private key
message = b'Hello, world!'
signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))

# Serialize the signature
r, s = decode_dss_signature(signature)
serialized_signature = encode_dss_signature(r, s)

private_key_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


# Verify the signature using the public key
try:
    print('private_key_pem', private_key_pem.decode('utf-8'),'/n')
    print('public_key_pem', public_key_pem.decode('utf-8'),'/n')
    public_key.verify(signature, message, ec.ECDSA(hashes.SHA256()))
    print('Signature is valid.')
except InvalidSignature:
    print('Signature is invalid.')
