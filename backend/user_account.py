import json
import hashlib
from copy import deepcopy
from pathlib import Path

DATA_DIR = Path("data")
USER_FILE = DATA_DIR / "users.json"


class UserAccount:
    """
    Represents a user account with hashed password storage.
    """

    def __init__(self, username, password_hash, email=None):
        self.username = deepcopy(username)
        self.password_hash = deepcopy(password_hash)  # store hash, not raw pw
        self.email = deepcopy(email)

    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        return self.password_hash == UserAccount.hash_password(password)

    def to_dict(self) -> dict:
        return {
            "username": self.username,
            "password_hash": self.password_hash,
            "email": self.email,
        }

    @staticmethod
    def from_dict(data: dict) -> "UserAccount":
        return UserAccount(
            data["username"],
            data["password_hash"],
            data.get("email")
        )

def load_users() -> dict[str, UserAccount]:
    """
    Load users from data/users.json.
    Returns: {username: UserAccount}
    """
    if not USER_FILE.exists():
        return {}

    with open(USER_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)

    return {u["username"]: UserAccount.from_dict(u) for u in raw}


def save_users(users: dict[str, UserAccount]) -> None:
    """
    Save user accounts to data/users.json.
    """
    DATA_DIR.mkdir(exist_ok=True)

    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump(
            [u.to_dict() for u in users.values()],
            f,
            indent=4
        )
