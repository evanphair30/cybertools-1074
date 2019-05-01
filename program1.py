#!/usr/bin/env python3.6

from csv import DictReader, DictWriter
from getpass import getpass
from hashlib import md5
from pathlib import Path
from sys import stderr as STDERR

PASSWORD_FILE = 'password.csv'
PASSWORD_FILE_FORMAT = ['username', 'password'] 

def register_user(username, password):
    if not username_exists(username):
        with open(PASSWORD_FILE, 'a') as csv:
            hashed_password = md5(str.encode(password)).hexdigest()
            writer = DictWriter(csv, fieldnames = PASSWORD_FILE_FORMAT)
            writer.writerow({'username': username, 'password': hashed_password})
        print('User registered')
    else:
        print('Username already registered', file = STDERR)

def prompt_password():
    return getpass()

def prompt_username():
    return input('Enter a username: ')

def username_exists(username):
    with open(PASSWORD_FILE, 'r') as csv:
        reader = DictReader(csv, PASSWORD_FILE_FORMAT)
        for row in reader:
            if row['username'] == username:
                return True
    return False

def init_password_file():
    path = Path(PASSWORD_FILE)
    path.touch(exist_ok = True)

def main():
    init_password_file()
    print('Beginning Registration...')
    username = prompt_username()
    password = prompt_password()
    register_user(username, password)

if __name__ == '__main__':
    main()
