"""Demo-grade cryptography for the Lethe demo: real primitives, not audited.

- Blind credentials: RSA-FDH blind signatures, the idea behind Privacy Pass
  (RFC 9474 / 9578; the RFCs use RSA-PSS). The issuer signs a value it cannot see,
  so it cannot later tell which credential a request spent.
- Sealed requests: X25519 + HKDF-SHA256 + ChaCha20-Poly1305, the shape of
  Oblivious HTTP (RFC 9458, HPKE). The relay carries bytes it cannot read.
- Padding: every sealed message is padded to a fixed size bucket, as in bitchat,
  so its length says little about its content.
"""
import hashlib
import math
import os
import secrets

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, x25519
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

BUCKETS = (1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144)
RAW = dict(encoding=serialization.Encoding.Raw, format=serialization.PublicFormat.Raw)


# ---------------------------------------------------------------- padding
def pad(data: bytes) -> bytes:
    size = next((b for b in BUCKETS if b > len(data)), None)
    if size is None:
        size = (len(data) // BUCKETS[-1] + 1) * BUCKETS[-1]
    return data + b"\x80" + b"\x00" * (size - len(data) - 1)


def unpad(data: bytes) -> bytes:
    body = data.rstrip(b"\x00")
    if not body.endswith(b"\x80"):
        raise ValueError("bad padding")
    return body[:-1]


# ---------------------------------------------------------------- blind credentials
def fdh(msg: bytes, n: int) -> int:
    """Full-domain hash: SHA-256 in counter mode, stretched to the modulus size."""
    k = (n.bit_length() + 7) // 8
    out, c = b"", 0
    while len(out) < k:
        out += hashlib.sha256(msg + c.to_bytes(4, "big")).digest()
        c += 1
    return int.from_bytes(out[:k], "big") % n


class IssuerKey:
    def __init__(self, bits: int = 2048):
        nums = rsa.generate_private_key(public_exponent=65537, key_size=bits).private_numbers()
        self.n, self.e, self._d = nums.public_numbers.n, nums.public_numbers.e, nums.d

    @property
    def key_id(self) -> str:
        return hashlib.sha256(self.n.to_bytes(256, "big")).hexdigest()[:16]

    def sign_blinded(self, blinded: list[int]) -> list[int]:
        return [pow(b, self._d, self.n) for b in blinded]


def blind(n: int, e: int):
    """Client side: pick a random credential and hide it before the issuer signs it."""
    nonce = secrets.token_bytes(32)
    while True:
        r = secrets.randbelow(n - 3) + 2
        if math.gcd(r, n) == 1:
            break
    return nonce, r, (fdh(nonce, n) * pow(r, e, n)) % n


def unblind(n: int, e: int, nonce: bytes, r: int, signed_blinded: int) -> int:
    sig = (signed_blinded * pow(r, -1, n)) % n
    if not verify(n, e, nonce, sig):
        raise ValueError("issuer returned a bad signature")
    return sig


def verify(n: int, e: int, nonce: bytes, sig: int) -> bool:
    return pow(sig, e, n) == fdh(nonce, n)


# ---------------------------------------------------------------- sealed requests (OHTTP-shaped)
def gateway_keypair():
    sk = x25519.X25519PrivateKey.generate()
    return sk, sk.public_key().public_bytes(**RAW)


def _keys(shared: bytes, enc: bytes, pk: bytes):
    def derive(info: bytes) -> bytes:
        return HKDF(algorithm=hashes.SHA256(), length=32, salt=enc + pk, info=info).derive(shared)
    return derive(b"lethe-demo request"), derive(b"lethe-demo response")


def seal_request(gateway_pk: bytes, plaintext: bytes):
    eph = x25519.X25519PrivateKey.generate()
    enc = eph.public_key().public_bytes(**RAW)
    shared = eph.exchange(x25519.X25519PublicKey.from_public_bytes(gateway_pk))
    k_req, k_res = _keys(shared, enc, gateway_pk)
    nonce = os.urandom(12)
    return enc + nonce + ChaCha20Poly1305(k_req).encrypt(nonce, pad(plaintext), None), k_res


def open_request(gateway_sk, gateway_pk: bytes, blob: bytes):
    enc, nonce, ct = blob[:32], blob[32:44], blob[44:]
    shared = gateway_sk.exchange(x25519.X25519PublicKey.from_public_bytes(enc))
    k_req, k_res = _keys(shared, enc, gateway_pk)
    return unpad(ChaCha20Poly1305(k_req).decrypt(nonce, ct, None)), k_res


def seal_response(k_res: bytes, plaintext: bytes) -> bytes:
    nonce = os.urandom(12)
    return nonce + ChaCha20Poly1305(k_res).encrypt(nonce, pad(plaintext), None)


def open_response(k_res: bytes, blob: bytes) -> bytes:
    return unpad(ChaCha20Poly1305(k_res).decrypt(blob[:12], blob[12:], None))
