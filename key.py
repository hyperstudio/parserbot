import hashlib
import string
import random

def generate_key():
    secret_key = ''.join(random.choice(string.hexdigits) for _ in range(32))
    secret_key_digest = hashlib.md5(secret_key).hexdigest()
    print "\n********************************"
    print ('Here is your secret key, place this in the `PARSERBOT_SECRET_KEY` '
        'environment variable: "%s"' % secret_key)
    print ('Here is the hash of your secret key, include this in the '
        '"Authorization" header of every request: "%s"' % secret_key_digest)
    print "********************************\n"

if __name__ == "__main__":
    generate_key()
