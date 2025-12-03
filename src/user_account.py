#  user_account.py
import json
import hashlib
from copy import deepcopy
from pathlib import Path

# persistent store for user accounts
USER_FILE = Path("users.json")


class UserAccount:
    """
    Represents a user account with hashed password storage.
    """

    def __init__(self, username, password_hash, email=None):
        self.username = deepcopy(username)
        self.password_hash = deepcopy(password_hash)  # store hash, not raw pw
        self.email = deepcopy(email)

    # hash helper (SHA-256)
    @staticmethod
    def hash_password(password: str) -> str:
        return hashlib.sha256(password.encode()).hexdigest()

    # verify plain password against stored hash
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
        return UserAccount(data["username"], data["password_hash"], data.get("email"))


# ------------------------------
# persistence helpers
# ------------------------------
def load_users() -> dict[str, UserAccount]:
    """
    Load users from users.json.
    Returns: {username: UserAccount}
    """
    if not USER_FILE.exists():
        return {}
    with open(USER_FILE, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return {u["username"]: UserAccount.from_dict(u) for u in raw}


def save_users(users: dict[str, UserAccount]) -> None:
    """
    Save users to users.json.
    """
    with open(USER_FILE, "w", encoding="utf-8") as f:
        json.dump([u.to_dict() for u in users.values()], f, indent=4)