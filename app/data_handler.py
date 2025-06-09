import os
import json
from typing import Dict, Any
from cryptography.fernet import Fernet
from app.config import FERNET_KEY


fernet = Fernet(FERNET_KEY.encode())

def encrypt_data(data: Dict[str, Any]) -> bytes:
    json_data = json.dumps(data).encode()
    return fernet.encrypt(json_data)

def decrypt_data(token: bytes) -> Dict[str, Any]:
    return json.loads(fernet.decrypt(token).decode())

def save_candidate_data(candidate_data: Dict[str, Any], filename: str = "data/candidate_data.enc") -> None:
    encrypted = encrypt_data(candidate_data)
    with open(filename, "ab") as f:  # append to allow multiple entries
        f.write(encrypted + b"\n")

def load_all_candidate_data(filename: str = "data/candidate_data.enc") -> list:
    data = []
    with open(filename, "rb") as f:
        for line in f:
            if line.strip():
                data.append(decrypt_data(line.strip()))
    return data
