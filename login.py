from getpass import getpass

from auth import verify_user, create_user

def signup():
    print("\n=== SIGN UP ===")
    username = input("Username: ").strip()
    if not username:
        print("Username is required.")
        return None, None
    password = getpass("Password: ").strip()
    if not password:
        print("Password is required.")
        return None, None
    uid = create_user(username, password)
    if uid:
        return uid, username
    return None, None

def login():
    print("\n=== LOGIN ===")
    username = input("Username: ").strip()
    password = getpass("Password: ").strip()
    uid = verify_user(username, password)
    if uid:
        return uid, username
    print("Invalid credentials.")
    return None, None