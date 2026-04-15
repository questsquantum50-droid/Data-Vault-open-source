import json
import os

from core.encryption import decrypt, encrypt

DATA_VAULT = "vault.json"
LEGACY_STORAGE_FILE = os.path.join("data", "vault.json")

DEFAULT_VAULT = {
    "auth": None,
    "recovery": None,
    "encrypted_key_master": None,
    "encrypted_key_recovery": None,
    "passwords": [],
}


def load_vault() -> dict:
    if not os.path.exists(DATA_VAULT):
        return DEFAULT_VAULT.copy()

    with open(DATA_VAULT, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return DEFAULT_VAULT.copy()

    if isinstance(data, list):
        return {
            "auth": None,
            "recovery": None,
            "encrypted_key_master": None,
            "encrypted_key_recovery": None,
            "passwords": data,
        }

    result = DEFAULT_VAULT.copy()
    result.update(data)
    result.setdefault("passwords", [])
    return result


def save_vault(data: dict) -> None:
    with open(DATA_VAULT, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


def _load_legacy_vault() -> dict:
    if not os.path.exists(LEGACY_STORAGE_FILE):
        return {}

    with open(LEGACY_STORAGE_FILE, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            return {}

    return data if isinstance(data, dict) else {}


def _save_legacy_vault(vault: dict) -> None:
    os.makedirs(os.path.dirname(LEGACY_STORAGE_FILE), exist_ok=True)
    with open(LEGACY_STORAGE_FILE, "w", encoding="utf-8") as f:
        json.dump(vault, f, indent=4)


def save_password(master_password: str, label: str, password: str) -> None:
    """
    Encrypts and saves a password under a label for the legacy storage flow.
    """
    vault = _load_legacy_vault()
    vault[label] = encrypt(master_password, password)
    _save_legacy_vault(vault)
    print(f"Password for '{label}' saved successfully!")


def get_password(master_password: str, label: str) -> str:
    """
    Retrieves and decrypts a password by label from the legacy storage flow.
    """
    vault = _load_legacy_vault()
    if label not in vault:
        raise KeyError(f"No password found for '{label}'")
    return decrypt(master_password, vault[label])


def list_labels() -> list:
    """
    Returns all saved password labels from the legacy storage flow.
    """
    vault = _load_legacy_vault()
    return list(vault.keys())


def delete_password(label: str) -> None:
    """
    Deletes a saved password by label from the legacy storage flow.
    """
    vault = _load_legacy_vault()
    if label not in vault:
        raise KeyError(f"No password found for '{label}'")
    del vault[label]
    _save_legacy_vault(vault)
    print(f"Password for '{label}' deleted!")
