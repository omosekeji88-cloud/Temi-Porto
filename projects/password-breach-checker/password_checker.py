
# cbfda is a hash function (not the entire hash, just a little bit of it)
# A hash function converts data into a fixed-length string. The same input always produces the same output, and it’s designed to be computationally difficult to reverse. They’re commonly used for password storage and data integrity checks.
# the count tells you how many times a password has been hacked


import requests
import hashlib
import sys

# import password module API URL + password

# k anonymity

def request_api_data(hashed_char):
    url = 'https://api.pwnedpasswords.com/range/' + hashed_char
    res = requests.get(url)
    if res.status_code != 200:
        raise RuntimeError(f'error fetching: {res.status_code}, check the api and try again')
    return res

# obtain hashes that match the beginning of the password
def get_password_leaks_count(hashes, hash_to_check):
    hashes = (line.split(':') for line in hashes.text.splitlines())
    for h, count in hashes:
        if h == hash_to_check:
            return count
    return 0


#password converted to hash
def pwned_api_check(password):
    sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    first5_char, tail = sha1password[:5], sha1password[5:]
    response = request_api_data(first5_char)
    return get_password_leaks_count(response, tail)

def main(args):
    for password in args:
        count = pwned_api_check(password)
        if count:
            print(f'{password} was found {count} times... you should probably change your password')
        else:
            print(f'{password} was not found carry on, it is safe')
    return 'done'

main(sys.argv[1:])
