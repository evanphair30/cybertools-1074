#!/usr/bin/env python3.6

from csv import DictReader, DictWriter
from getpass import getpass
from hashlib import md5
from pathlib import Path
from sys import stderr as STDERR

def evaluate_password(password, dictionary):
    if is_weak(password, dictionary):
        print('Your password is WEAK. Consider another one.')
    elif is_moderate(password, dictionary):
        print('Your password is MODEATE. Consider another one.')
    else:
        print('Your password is STRONG. Good Job.')

def is_moderate(password, dictionary):
    return len([word for word in dictionary if password in word]) > 0

def is_weak(password, dictionary):
    return len(password)<=2 or password in dictionary

def prompt_password():
    return getpass()

def init_dict():
    with open('dictionary.txt', mode='r') as infile:
        return [word.strip('\n') for word in infile]

def main():
    dictionary = init_dict()
    password = prompt_password()
    evaluate_password(password, dictionary)

if __name__ == '__main__':
    main()
