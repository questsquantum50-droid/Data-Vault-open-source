import hashlib
import json
import os

import bcrypt
from cryptography.hazmat.primitives import constant_time

from core.encryption import decrypt, encrypt

AUTH_FILE = os.path.join("data", "auth.json")
BCRYPT_ROUNDS = 12
HASH_ITERATIONS = 600_000
KEY_LEN = 32


def normalize_text(value: str) -> str:
    return value.strip().lower()


def _hash_with_bcrypt(password: str) -> str:
    hashed = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=BCRYPT_ROUNDS),
    )
    return hashed.decode("utf-8")


def _verify_legacy_pbkdf2(password: str, auth_data: dict) -> bool:
    try:
        salt = bytes.fromhex(auth_data["salt"])
        expected = bytes.fromhex(auth_data["hash"])
    except (KeyError, TypeError, ValueError):
        return False

    test = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt,
        auth_data.get("iterations", HASH_ITERATIONS),
        dklen=KEY_LEN,
    )
    return constant_time.bytes_eq(test, expected)


def hash_master_password(password: str) -> dict:
    return {
        "scheme": "bcrypt",
        "password_hash": _hash_with_bcrypt(password),
    }


def verify_master_password(password: str, auth_data: dict) -> bool:
    if not password or not isinstance(auth_data, dict):
        return False

    stored_hash = auth_data.get("password_hash")
    if stored_hash is not None:
        try:
            return bcrypt.checkpw(
                password.encode("utf-8"),
                stored_hash.encode("utf-8"),
            )
        except (AttributeError, TypeError, ValueError):
            return False

    if "salt" in auth_data and "hash" in auth_data:
        return _verify_legacy_pbkdf2(password, auth_data)

    return False


def _load_auth_file() -> dict | None:
    if not os.path.exists(AUTH_FILE):
        return None

    with open(AUTH_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return None

    return data if isinstance(data, dict) else None


def _save_auth_file(auth_data: dict) -> None:
    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(auth_data, f, indent=4)


def register(master_password: str) -> bool:
    """
    Hashes and saves the master password.
    Returns False if user already exists.
    """
    if _load_auth_file() is not None:
        print("User already registered!")
        return False

    _save_auth_file(hash_master_password(master_password))
    print("Master password set successfully!")
    return True


def login(master_password: str) -> bool:
    """
    Verifies master password against stored hash.
    Returns True if correct, False if wrong.
    """
    auth_data = _load_auth_file()
    if auth_data is None:
        print("No user registered yet!")
        return False

    return verify_master_password(master_password, auth_data)


def build_recovery_secret(mode: str, answers: list) -> str:
    if mode == "text":
        return "|".join(normalize_text(answer) for answer in answers)
    return "|".join(str(answer) for answer in answers)


def verify_recovery_answers(recovery_data: dict, answers: list) -> bool:
    if recovery_data is None:
        return False
    if recovery_data["mode"] == "text":
        expected = [normalize_text(value) for value in recovery_data["answers"]]
        return [normalize_text(value) for value in answers] == expected

    try:
        return [int(value) for value in answers] == recovery_data.get("correct", [])
    except (TypeError, ValueError):
        return False


def derive_recovery_secret(recovery_data: dict, answers: list) -> str:
    return build_recovery_secret(recovery_data["mode"], answers)


def encrypt_vault_key(master_secret: str, vault_key_hex: str) -> dict:
    return encrypt(master_secret, vault_key_hex)


def decrypt_vault_key(master_secret: str, encrypted_key: dict) -> str:
    return decrypt(master_secret, encrypted_key)
