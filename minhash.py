import sys
import random
import binascii
import time

HASH_NUM = 1000
# 32 byte hash
MAX_SHINGLE_ID = 2**32-1
# PRIME is the next prime greater than MAX_SHINGLE_ID
PRIME = 4294967311
SHINGLE_SIZE = 3
SHINGLE_TYPE = 3
# SHINGLE_TYPE is 'word' or 'char'
SHINGLE_TYPE = 'word'

def HASH_FUNC(x):
    return binascii.crc32(x.encode('utf-8')) & 0xffffffff

def calculate(
    s1, s2, coeffs_a=None, coeffs_b=None, total_hash_num=HASH_NUM,
    max_shingle_id=MAX_SHINGLE_ID, shingle_size=SHINGLE_SIZE,
    shingle_type=SHINGLE_TYPE, hash_func=HASH_FUNC, prime=PRIME
    ):
    if type(s1) == str:
        # if string, turn to shingles
        shingles1 = str_to_shingles(s1, shingle_size=shingle_size, shingle_type=shingle_type)
        shingles2 = str_to_shingles(s2, shingle_size=shingle_size, shingle_type=shingle_type)

    elif type(s1) == list or type(s1) == set:
        # HACK: assuming shingles
        shingles1 = s1
        shingles2 = s2

    if not coeffs_a:
        coeffs_a = generate_coefficients(total_hash_num=total_hash_num, max_shingle_id=max_shingle_id)
        coeffs_b = generate_coefficients(total_hash_num=total_hash_num, max_shingle_id=max_shingle_id)

    sigs_a = get_min_signatures(shingles1, coeffs_a, coeffs_b, total_hash_num=total_hash_num, hash_func=hash_func)
    sigs_b = get_min_signatures(shingles2, coeffs_a, coeffs_b, total_hash_num=total_hash_num, hash_func=hash_func)

    union_count = 0
    for i, val in enumerate(sigs_a):
        if sigs_b[i] == val:
            union_count += 1

    return union_count / float(total_hash_num)

def get_min_signatures(shingles, coeffs_a, coeffs_b, total_hash_num=HASH_NUM, hash_func=HASH_FUNC, prime=PRIME):
    min_signatures = list()
    hash_count = 0

    while hash_count < total_hash_num:
        min_hash = prime + 1
        for shingle in shingles:
            # hash function is (a*x + b) % c
            # Where 'x' is the input value, 'a' and 'b' are random coefficients, and 'c' is our prime num
            current_hash = (coeffs_a[hash_count] * hash_func(shingle) + coeffs_b[hash_count]) % prime

            if current_hash < min_hash:
                min_hash = current_hash

        min_signatures.append(min_hash)
        hash_count += 1

    return min_signatures

def str_to_shingles(string, shingle_size=SHINGLE_SIZE, shingle_type=SHINGLE_TYPE):
    shingles_in_doc = set()

    if shingle_type == 'word':
        units = string.split(' ')
    elif shingle_type == 'char':
        units = list(string)

    for idx in range(0, len(units) - (shingle_size - 1)):
        shingle = ''.join(units[idx:idx+shingle_size])
        shingles_in_doc.add(shingle)

    return list(shingles_in_doc)

def generate_coefficients(total_hash_num=HASH_NUM, max_shingle_id=MAX_SHINGLE_ID):
    # create a unique set of 'HASH_NUM' random values
    rand_set = set()
    hash_num = 0

    while hash_num < total_hash_num:
        rand_num = random.randint(0, max_shingle_id)
        rand_set.add(rand_num)

        # if rand_num not added, it means that it already exists in set
        # Try again.
        if len(rand_set) - 1 == hash_num:
            hash_num += 1

    return list(rand_set)

if __name__ == '__main__':
    str_one, str_two = ['','']
    with open(sys.argv[1], 'rb+') as f:
        str_one = f.read()

    with open(sys.argv[2], 'rb+') as f:
        str_two = f.read()

    sys.stdout.write(calculate(str_one, str_two))
