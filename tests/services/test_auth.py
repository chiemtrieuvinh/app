import pytest
from schemas.user import get_password_hash, verify_password

def test_get_password_hash():
    password = "test123"
    hashed = get_password_hash(password)
    assert hashed != password
    assert hashed.startswith("$2b$")


def test_get_password_hash_empty():
    hashed = get_password_hash("")
    assert hashed.startswith("$2b$")


def test_get_password_hash_special_chars():
    password = "!@#$%^&*()_+"
    hashed = get_password_hash(password)
    assert hashed != password
    assert hashed.startswith("$2b$")


def test_get_password_hash_unique():
    password = "same_password"
    hash1 = get_password_hash(password)
    hash2 = get_password_hash(password)
    assert hash1 != hash2


def test_verify_password():
    password = "test123"
    hashed = get_password_hash(password)
    assert verify_password(password, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_verify_password_empty():
    hashed = get_password_hash("")
    assert verify_password("", hashed) is True
    assert verify_password("nonempty", hashed) is False


def test_verify_password_case_sensitive():
    password = "Test123"
    hashed = get_password_hash(password)
    assert verify_password("Test123", hashed) is True
    assert verify_password("test123", hashed) is False


def test_verify_password_invalid_hash():
    with pytest.raises(Exception):
        verify_password("password", "invalid_hash")