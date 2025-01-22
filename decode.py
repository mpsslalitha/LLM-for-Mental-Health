import pickle

# Path to the user database file
USER_DB = "user_db.pkl"

try:
    # Load the user database
    with open(USER_DB, "rb") as f:
        users = pickle.load(f)
    
    # Display the user data
    print("User Database:")
    for username, hashed_password in users.items():
        print(f"Username: {username}, Hashed Password: {hashed_password}")
except FileNotFoundError:
    print(f"The file '{USER_DB}' does not exist.")
except Exception as e:
    print(f"An error occurred while reading the user database: {e}")


