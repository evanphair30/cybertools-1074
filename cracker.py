#!/usr/bin/env python3.6
import argparse
import time
from hashlib import md5
from itertools import chain
from pathlib import Path
from sys import stderr as STDERR

SPECIAL_CHARS = list(range(0,10)) + [ '!', '@', '#', '$', '%' ]

def crack_with_three_special_chars(password, dictionary_file):
    with open(dictionary_file, 'r') as dictionary:
        for word in dictionary: 
            word = word.strip('\n')
            for x in range(len(word) + 1):
                for sc in SPECIAL_CHARS:
                    special_word = '{}{}{}'.format(word[0:x] , sc , word[x:])
                    for y in range(len(special_word) + 1):
                        for sc2 in SPECIAL_CHARS:
                            special_word2 = '{}{}{}'.format(special_word[0:y] , sc2 , special_word[y:])
                            for z in range(len(special_word2) + 1):
                                for sc3 in SPECIAL_CHARS:
                                    special_word3 = '{}{}{}'.format(special_word2[0:z] , sc3 , special_word2[z:])
                                    hashed_word = md5(str.encode(special_word3)).hexdigest()
                                    if hashed_word == password: 
                                        return special_word3

def crack_with_two_special_chars(password, dictionary_file):
    with open(dictionary_file, 'r') as dictionary:
        for word in dictionary: 
            word = word.strip('\n')
            for x in range(len(word) + 1):
                for sc in SPECIAL_CHARS:
                    special_word = '{}{}{}'.format(word[0:x] , sc , word[x:])
                    for y in range(len(special_word) + 1):
                        for sc2 in SPECIAL_CHARS:
                            special_word2 = '{}{}{}'.format(special_word[0:y] , sc2 , special_word[y:])
                            hashed_word = md5(str.encode(special_word2)).hexdigest()
                            if hashed_word == password: 
                                return special_word2

def crack_with_one_special_chars(password, dictionary_file):
    with open(dictionary_file, 'r') as dictionary:
        for word in dictionary: 
            word = word.strip('\n')
            for x in range(len(word) + 1):
                for sc in SPECIAL_CHARS:
                    special_word = '{}{}{}'.format(word[0:x] , sc , word[x:])
                    hashed_word = md5(str.encode(special_word.strip('\n'))).hexdigest()
                    if hashed_word == password: 
                        return special_word

def crack_with_dict(password, dictionary_file):
    with open(dictionary_file, 'r') as dictionary:
        for word in dictionary: 
            hashed_word = md5(str.encode(word.strip('\n'))).hexdigest()
            if hashed_word == password: 
                return word
    return None

def crack(password, dictionary_file):
    cracked = crack_with_dict(password, dictionary_file)
    if not cracked:
        cracked = crack_with_one_special_chars(password, dictionary_file)
    if not cracked:
        cracked = crack_with_two_special_chars(password, dictionary_file)
    if not cracked:
        cracked = crack_with_three_special_chars(password, dictionary_file)
    return cracked

def read_password(filename):
    with open(filename, 'r') as f:
        return f.readline().strip('\n')

def valid_args(password_file, dictionary_file):
    return Path(password_file).exists and Path(dictionary_file).exists()

def perror(message):
    print('Error: {}'.format(message), file = STDERR)
    exit(1)

def main():
    parser = argparse.ArgumentParser(
            description = 'Use the dictionary file to crack a users password'
    )
    parser.add_argument('password_file', type=str,
        help = 'A file containing the hashed password'
    )
    parser.add_argument('dictionary_file', type=str,
        help = 'A file containing a subset of dictionary words to use when cracking the password'
    )
    args = parser.parse_args(args)

    password_file = args.password_file
    dictionary_file = args.dictionary_file
    if not valid_args(password_file, dictionary_file): perror('Invalid args')

    password = read_password(password_file)
    if not password: perror('No password in file.')

    start_time = time.time()
    cracked = crack(password, dictionary_file)
    end_time = time.time()
    if not cracked:
        print('Shucks... unable to crack password')
    else:
        print('Jackpot... the password is {} and it took {:.2f} seconds to crack '.format(cracked, end_time - start_time))


if __name__ == '__main__':
    main()
