#!/usr/bin/env python3.6

from csv import DictReader, DictWriter
from getpass import getpass
from hashlib import md5
from pathlib import Path
from program1 import PASSWORD_FILE, PASSWORD_FILE_FORMAT, prompt_username, prompt_password
from sys import stderr as STDERR

def login(username, password):
    with open(PASSWORD_FILE, "r") as csv:
        reader = DictReader(csv, PASSWORD_FILE_FORMAT)
        for row in reader:
            if row['username'] == username:
                hashed_password = md5(str.encode(password)).hexdigest()
                if hashed_password == row['password']:
                    print('Login Successful')
                    return
    print('Login Failed', file = STDERR)

def validate_password_file():
    path = Path(PASSWORD_FILE)
    if not path.exists():
        print('No pasword file exists to authenticate against...', file = STDERR) 
        print('Try running program1.py to register a user.', file = STDERR) 
        exit(1)

def main():
    validate_password_file()
    print('Login to your account')
    username = prompt_username()
    password = prompt_password()
    login(username, password)

if __name__ == '__main__':
    main()
