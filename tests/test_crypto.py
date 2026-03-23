"""Testes do módulo de descriptografia JWE."""

import base64
import json

import pytest
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

from app.core.crypto import MessageDecryptor


def _generate_test_jwk() -> str:
    """Gera JWK de teste com chave RSA válida."""
    key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    priv = key.private_numbers()

    def _to_b64url(n: int) -> str:
        data = n.to_bytes((n.bit_length() + 7) // 8, "big")
        return base64.urlsafe_b64encode(data).decode().rstrip("=")

    jwk = {
        "kty": "RSA",
        "kid": "test-key-id",
        "use": "enc",
        "alg": "RSA-OAEP-256",
        "e": _to_b64url(priv.public_numbers.e),
        "n": _to_b64url(priv.public_numbers.n),
        "d": _to_b64url(priv.d),
        "p": _to_b64url(priv.p),
        "q": _to_b64url(priv.q),
        "dp": _to_b64url(priv.dmp1),
        "dq": _to_b64url(priv.dmq1),
        "qi": _to_b64url(priv.iqmp),
    }
    return json.dumps(jwk)


def test_load_valid_jwk() -> None:
    """Testa carregamento de JWK válido."""
    test_jwk = _generate_test_jwk()
    decryptor = MessageDecryptor(test_jwk)
    assert decryptor.private_key is not None


def test_load_invalid_jwk_json() -> None:
    """Testa erro com JSON inválido."""
    with pytest.raises(ValueError, match="JSON malformado"):
        MessageDecryptor("invalid json")


def test_load_jwk_missing_fields() -> None:
    """Testa erro com campos obrigatórios ausentes."""
    invalid_jwk = json.dumps({"kty": "RSA"})
    with pytest.raises(ValueError, match="Campos obrigatórios ausentes"):
        MessageDecryptor(invalid_jwk)


def test_decrypt_invalid_jwe() -> None:
    """Testa erro com JWE inválido."""
    test_jwk = _generate_test_jwk()
    decryptor = MessageDecryptor(test_jwk)
    with pytest.raises(ValueError, match="Falha na descriptografia"):
        decryptor.decrypt_message("invalid_jwe_token")
