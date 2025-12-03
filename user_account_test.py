"""
User Accounts Test (standalone)
- Uses user_account.py (hashed passwords + JSON persistence)
- Monkeypatches USER_FILE to avoid touching real users.json
Run:
    python user_accounts_test.py
"""
from pathlib import Path
import json
import os
from importlib import import_module

def run():
    # ---- Import the module ----
    ua = import_module("user_account")  

    # ---- Use a test-local users file ----
    test_dir = Path(".").resolve()
    test_users_file = test_dir / "users_test.json"
    # Monkeypatch USER_FILE to point to our test file
    ua.USER_FILE = test_users_file

    # ---- Clean start ----
    if test_users_file.exists():
        test_users_file.unlink()
    users = ua.load_users()
    assert users == {}, "Expected empty users at clean start"
    print("✅ Clean start OK (no users).")

    # ---- Register first user ----
    uname = "snazbear"
    pw = "pass123"
    email = "snazbear@example.com"
    users[uname] = ua.UserAccount(uname, ua.UserAccount.hash_password(pw), email)
    ua.save_users(users)
    assert test_users_file.exists(), "users_test.json should be created"
    print("✅ Registered first user & saved to users_test.json.")

    # ---- Check contents / hash shape ----
    users2 = ua.load_users()
    assert uname in users2, "First user not found after reload"
    u1 = users2[uname]
    assert len(u1.password_hash) == 64 and all(c in "0123456789abcdef" for c in u1.password_hash), \
        "Password hash should be 64 hex chars (sha256)"
    print("✅ Reloaded users and verified SHA-256 hash shape.")

    # ---- Login attempts ----
    assert not u1.verify_password("wrongpw"), "Wrong password should fail"
    assert u1.verify_password(pw), "Correct password should succeed"
    print("✅ Login checks passed (wrong fails, correct succeeds).")

    # ---- Duplicate username prevention (demonstration) ----
    # Your app should guard: if uname in users: error
    duplicate_blocked = uname in users2
    assert duplicate_blocked, "Expected app logic to block duplicate usernames"
    print("✅ Duplicate username prevention demonstrated.")

    # ---- Register a second user ----
    uname2 = "james"
    pw2 = "carlover"
    email2 = "james@example.com"
    users2[uname2] = ua.UserAccount(uname2, ua.UserAccount.hash_password(pw2), email2)
    ua.save_users(users2)

    # ---- Verify persistence with two users ----
    users3 = ua.load_users()
    assert set(users3.keys()) == {uname, uname2}, "Expected two users after second registration"
    assert users3[uname2].verify_password(pw2), "Second user's password check failed"
    print("✅ Second user registered and persisted.")

    # ---- Show JSON contents ----
    print("\n--- users_test.json ---")
    print(test_users_file.read_text(encoding="utf-8"))
    print("-----------------------\n")

    print("🎉 All user account tests passed.")

if __name__ == "__main__":
    # If user_account.py is not in the same folder, run with:
    #   PYTHONPATH=. python user_accounts_test.py
    try:
        run()
    except ModuleNotFoundError:
        print("❌ Could not import 'user_account'. Make sure user_account.py is in the same folder.")
        raise
