import bcrypt

# Raw password to hash (e.g., from form)
plain_password = "202100456".encode('utf-8')

# Hash with automatic salt
hashed_password = bcrypt.hashpw(plain_password, bcrypt.gensalt())

# Save hashed_password.decode('utf-8') in your JSON database
print(hashed_password.decode('utf-8'))

